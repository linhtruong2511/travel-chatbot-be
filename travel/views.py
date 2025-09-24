from rest_framework import viewsets
from .serializers import TourSerializer
from .models import Tour
# Create your views here.

class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
