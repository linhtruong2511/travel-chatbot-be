from numpy.f2py.auxfuncs import throw_error
from rest_framework import viewsets, status
from rest_framework.views import APIView

from .serializers import TourSerializer, CommentSerializer
from .models import Tour
from rest_framework.response import Response
# Create your views here.

class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer

class CommentAPI(APIView):
    def post(self, request, *args, **kwargs):
        print('data', request.data)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

