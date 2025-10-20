from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ItineraryListCreateView, ItineraryDetailView, ChangeStatus, GetAllItinerary, CommentViewSet, \
    LikeViewSet

router = DefaultRouter()
router.register('comments', CommentViewSet, basename='comments')
router.register('likes', LikeViewSet, basename='likes')
urlpatterns = [
    path('', ItineraryListCreateView.as_view(), name='itinerary-list-create'),
    path('<uuid:pk>/', ItineraryDetailView.as_view(), name='itinerary-detail'),
    path('update-status/<uuid:pk>/', ChangeStatus.as_view(), name='itinerary-update-status'),
    path('get-all/', GetAllItinerary.as_view(), name='itinerary-get-all'),
    # path('like/<uuid:pk>/<bool:up>', LikeItineraryView.as_view(), name='itinerary-like'),
    # path('dislike/<uuid:pk>/<bool:up>', DislikeItineraryView.as_view(), name='itinerary-get-all'),
] + router.urls