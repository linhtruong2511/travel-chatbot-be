from rest_framework import viewsets, status
from .serializers import TourSerializer
from .models import Tour
from rest_framework.response import Response
# Create your views here.

class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
