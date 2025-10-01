import re
import json
from typing import Any, Dict, Optional, List, Tuple
from openai import OpenAI
import os
from travel.models import Tour


def extract_json_from_text(text_or_obj: Any) -> Dict:
    """
    LLM may return a dict or a string containing JSON (maybe wrapped in markdown).
    This function attempts to return a Python dict.
    """
    if isinstance(text_or_obj, dict):
        return text_or_obj
    if not isinstance(text_or_obj, str):
        raise ValueError("Unexpected type for LLM content")

    # Find the first JSON object {...}
    m = re.search(r"\{.*\}", text_or_obj, re.DOTALL)
    to_parse = m.group(0) if m else text_or_obj

    try:
        return json.loads(to_parse)
    except Exception:
        # Try to be forgiving: replace single quotes with double quotes (best-effort)
        try:
            return json.loads(to_parse.replace("'", '"'))
        except Exception as e:
            raise ValueError(f"Không thể parse JSON từ LLM response: {e}\nRAW:\n{to_parse}")


def parse_price_to_vnd(val: Any) -> Optional[int]:
    """
    Normalize price expressions returned by LLM to integer VND (max price).
    Accept ints, strings like "5 triệu", "4-5 triệu", "5000000", etc.
    """
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return int(val)

    s = str(val).lower().strip()
    # handle range "4-5 triệu" -> take upper bound
    range_match = re.search(r"(\d+\.?\d*)\s*[-–to]\s*(\d+\.?\d*)\s*(triệu|m|k|vnđ)?", s)
    if range_match:
        upper = float(range_match.group(2))
        unit = range_match.group(3) or ""
        if "triệu" in unit or "m" in unit:
            return int(upper * 1_000_000)
        if "k" in unit:
            return int(upper * 1_000)
        if "vnđ" in unit or unit == "":
            return int(upper)

    # single number like "5 triệu" or "5000000"
    m = re.search(r"(\d+\.?\d*)\s*(triệu|m|k|vnđ)?", s)
    if m:
        num = float(m.group(1))
        unit = m.group(2) or ""
        if "triệu" in unit or "m" in unit:
            return int(num * 1_000_000)
        if "k" in unit:
            return int(num * 1_000)
        return int(num)
    return None


def normalize_duration(dur: Any) -> Optional[List[int]]:
    """
    Normalize duration field to a list of integers (e.g., 3 -> [3], "3-4" -> [3,4], [3,4] -> [3,4])
    """
    if dur is None:
        return None
    if isinstance(dur, list):
        try:
            return [int(x) for x in dur]
        except Exception:
            pass
    if isinstance(dur, int):
        return [dur]
    s = str(dur)
    # find numbers
    nums = re.findall(r"\d+", s)
    if not nums:
        return None
    return [int(n) for n in nums]


# -----------------------
# LLM parse function
# -----------------------
def parse_with_llm(user_query: str) -> Dict:
    api_key = os.environ.get("OPENAI_KEY")
    client = OpenAI(api_key=api_key)
    if not api_key:
        raise RuntimeError("Missing OpenAI API key")

    prompt = f"""
Bạn là hệ thống phân tích yêu cầu du lịch. Trả về đúng **một JSON thuần** (không văn bản khác)
với các field:
- duration: số ngày (int hoặc list nếu khoảng). Ví dụ 3 hoặc [3,4]
- max_price: ngân sách tối đa (int, VND). Ví dụ 5000000
- min_price: ngân sách tối thiểu (int, VND). Ví dụ 3000000
- tags: danh sách từ khóa (ví dụ: ["biển","gia đình"])
- location: địa điểm khu du lịch (ví dụ: Nha trang, Hạ Long)
- others: chuỗi hoặc object với thông tin bổ sung nếu có, null nếu không có.

Câu hỏi: \"{user_query}\"
"""

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            response_format={"type": "json_object"}
        )
    except Exception as e:
        raise RuntimeError(f"LLM parse error: {e}")

    # Lấy content (SDK có thể trả dict hoặc string)
    content = resp.choices[0].message.content

    parsed_raw = extract_json_from_text(content)

    # print('parsed_raw:', parsed_raw)

    # Normalize fields
    duration = normalize_duration(parsed_raw.get("duration"))
    max_price = parse_price_to_vnd(parsed_raw.get("max_price"))
    min_price = parse_price_to_vnd(parsed_raw.get("min_price"))
    location = parsed_raw.get("location")

    tags = parsed_raw.get("tags") or []
    if isinstance(tags, str):
        # split by comma if LLM returned a string
        tags = [t.strip() for t in re.split(r"[;,]", tags) if t.strip()]
    tags = [t.lower() for t in tags]

    print('raw: ', parsed_raw)

    return {
        "duration": duration,
        "max_price": max_price,
        "tags": tags,
        "others": parsed_raw.get("others"),
        'min_price': min_price,
        'location': location,
        # keep raw for debugging
        "_raw": parsed_raw
    }


def score_and_rank(tours: List[Tour], parsed: Dict, top_k: int = 5) -> List[Tuple[Tour, float]]:
    results = []

    for t in tours:
        # duration match
        if parsed["duration"] is None or parsed["duration"] is None:
            duration_ok = True
        else:
            duration_ok = t.duration in parsed["duration"]

        # price match
        if t.max_budget is None or parsed["max_price"] is None:
            max_price_ok = True
        else:
            max_price_ok = t.max_budget <= parsed["max_price"]

        if t.min_budget is None or parsed["min_price"] is None:
            min_price_ok = True
        else:
            min_price_ok = t.min_budget >= parsed["min_price"]

        if parsed["location"] is None:
            print("location pass because not provide location")
            location_ok = True
        else:
            print("location filing")
            location_ok = t.location.lower() in parsed["location"].lower() and t.location != ""

        print("location_ok: ", location_ok)


        # tag similarity score (0..1)
        if parsed["tags"]:
            matched = sum(1 for tag in parsed["tags"] if tag in t.tags.split(','))
            tag_score = matched / len(parsed["tags"])
        else:
            tag_score = 0.5  # neutral if user didn't specify

        rating_norm = float(t.rate) / 5.0

        # Weighted scoring
        # weights: duration 0.35, price 0.30, tags 0.25, rating 0.10
        s = (0.35 * (1.0 if duration_ok else 0.0) +
             0.30 * (1.0 if max_price_ok else 0.0) +
             0.25 * tag_score +
             0.10 * rating_norm)

        # Only include tours that satisfy basic constraints (duration & price)
        if duration_ok and max_price_ok and min_price_ok and location_ok:
            results.append((t, s))

    results.sort(key=lambda x: x[1], reverse=True)

    print('results count:', len(results))

    return results[:top_k]


def generate_reply_with_llm(user_query: str, parsed: Dict, top_results: List[Tuple[Tour, float]]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_KEY"))
    # Format top_results into a short bullet list for LLM
    if not top_results:
        instructions = ("Mình không tìm thấy tour phù hợp với yêu cầu. Hãy trả lời ngắn gọn "
                        "và đề xuất hai cách: (1) nới ngân sách/độ dài, hoặc (2) gợi ý điểm tương tự.")
        messages = [
            {"role": "user",
             "content": f"User query: {user_query}\nParsed: {json.dumps(parsed, ensure_ascii=False)}\n\n{instructions}"}
        ]
    else:
        tours_text = ""
        for t, score in top_results:
            tours_text += f"- {t.name} | {t.duration} ngày | {t.min_budget:,} VND | {t.max_budget:,} VND | rating {t.rate}| desc: {t.short_description[0:255]} | tags: {t.tags}\n"
        messages = [
            {"role": "user", "content":
                f"Bạn là trợ lý du lịch. Người dùng hỏi: {user_query}\n\nParsed: {json.dumps(parsed, ensure_ascii=False)}\n\nTop matches:\n{tours_text}\n\nHãy trả lời bằng tiếng Việt, thân thiện, ngắn gọn: tóm tắt 5-7 câu, nêu 4 - 5 lựa chọn hàng đầu (tên, giá, 1 lý do), và khuyến nghị (nên chọn nếu thích gì)."}
        ]

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.2,
            max_tokens=400
        )
    except Exception as e:
        return f"Lỗi khi gọi LLM để sinh câu trả lời: {e}"

    return resp.choices[0].message.content.strip()
