from django.urls import path
from .views import ItineraryListCreateView, ItineraryDetailView

urlpatterns = [
    path('', ItineraryListCreateView.as_view(), name='itinerary-list-create'),
    path('<uuid:pk>/', ItineraryDetailView.as_view(), name='itinerary-detail'),
]