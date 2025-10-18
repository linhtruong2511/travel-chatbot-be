from django.urls import path
from .views import ItineraryListCreateView, ItineraryDetailView, ChangeStatus, GetAllItinerary

urlpatterns = [
    path('', ItineraryListCreateView.as_view(), name='itinerary-list-create'),
    path('<uuid:pk>/', ItineraryDetailView.as_view(), name='itinerary-detail'),
    path('update-status/<uuid:pk>/', ChangeStatus.as_view(), name='itinerary-update-status'),
    path('get-all/', GetAllItinerary.as_view(), name='itinerary-get-all'),
]