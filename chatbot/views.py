from travel.models import Tour
from rest_framework import views 
from .utils import parse_with_llm, score_and_rank, generate_reply_with_llm
from rest_framework.response import Response

# Create your views here.
class Chatbot(views.APIView):
    def get(self, request, *args, **kwargs):
        tours = Tour.objects.all()
        q = request.query_params.get("q")
        try:
            parsed = parse_with_llm(q)
             # 2) filter & rank
            top = score_and_rank(tours, parsed, top_k=5)
            reply = generate_reply_with_llm(q, parsed, top)
            print('reply', reply)
            return Response({"reply": reply})
            
        except Exception as e:
            print("Lỗi parse yêu cầu:", e)

        