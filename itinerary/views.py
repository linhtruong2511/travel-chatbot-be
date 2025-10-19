from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.views import APIView
from .models import Itinerary
from .serializers import ItinerarySerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework import status
class ItineraryListCreateView(generics.ListCreateAPIView):
    queryset = Itinerary.objects.all()
    serializer_class = ItinerarySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        itineraries = self.queryset.filter(author=request.user)
        page = self.paginate_queryset(itineraries)
        if page is not None:
            serializer = ItinerarySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(ItinerarySerializer(itineraries, many=True).data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ItineraryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Itinerary.objects.all()
    serializer_class = ItinerarySerializer

class ChangeStatus(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def patch(self, request, *args, **kwargs):
        itinerary = Itinerary.objects.get(pk=kwargs['pk'])
        itinerary.is_public = request.data.get('is_public')
        itinerary.save()
        return Response(status=status.HTTP_200_OK)

class GetAllItinerary(generics.ListAPIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        itineraries = Itinerary.objects.filter(is_public=True)
        page = self.paginate_queryset(itineraries)
        if page is not None:
            serializer = ItinerarySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(ItinerarySerializer(itineraries, many=True).data)
