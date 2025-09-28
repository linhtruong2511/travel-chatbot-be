import pandas as pd
from sqlalchemy import create_engine, Column, Integer, BigInteger, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --- ORM Base ---
Base = declarative_base()

class Tour(Base):
    __tablename__ = "travel_tour"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    duration = Column(Integer, nullable=False)             # số ngày
    duration_detail = Column(String(100), nullable=False)  # ví dụ: 3N2Đ
    tags = Column(String(100), nullable=False)
    thumbnail = Column(String(100))
    min_budget = Column(Integer, nullable=False)
    max_budget = Column(Integer, nullable=False)
    budget_detail = Column(String, nullable=False)
    budget_current = Column(String, nullable=False)
    rate = Column(Float, nullable=False)                   # numeric(5,2)
    description = Column(Text, nullable=False)
    note = Column(Text, nullable=False)


# --- Kết nối Postgres ---
DB_USER = "travel_user"
DB_PASS = "travel_pass"
DB_NAME = "travel_db"
DB_HOST = "localhost"
DB_PORT = "5432"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

Session = sessionmaker(bind=engine)
session = Session()

# --- Đọc Excel ---
file_url = "./tours_cleaned.xlsx"
df = pd.read_excel(file_url)


def parse_number(value):
    """Chuyển '2.000.000' -> 2000000 (int)."""
    if pd.isna(value):
        return 0
    if isinstance(value, (int, float)):
        return int(value)
    try:
        return int(str(value).replace(".", "").replace(",", "").strip())
    except:
        return 0


# --- Import dữ liệu ---
for _, row in df.iterrows():
    try:
        name = str(row.get("name", "")).replace("\n", " ")
        duration_detail = str(row.get("time_detail", "")).strip()

        # Lấy số ngày từ duration_detail (vd: "3N2Đ" -> 3)
        duration = 0
        if duration_detail:
            try:
                duration = int(''.join([c for c in duration_detail if c.isdigit()][:1]))
            except:
                duration = 0

        tour = Tour(
            name=name,
            duration=duration,
            duration_detail=duration_detail,
            tags=str(row.get("tags", "")),
            thumbnail=str(row.get("thumbnail", "")),
            min_budget=parse_number(row.get("min_budget", 0)),
            max_budget=parse_number(row.get("max_budget", 0)),
            budget_detail=str(row.get("budget_detail", "")),
            budget_current=str(row.get("budget_current", "")),
            rate=float(row.get("rate", 0) or 0),
            description=str(row.get("description", "")),
            note=str(row.get("note", "")),
        )

        session.add(tour)

    except Exception as e:
        print(f"❌ Failed to parse row:\n{row}\nError: {e}")
        break

# Commit dữ liệu vào DB
session.commit()
print("✅ Import thành công dữ liệu từ Excel vào Postgres!")
