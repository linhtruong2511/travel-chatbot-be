from django.urls import path
from .views import TourViewSet, CommentAPI
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tours', TourViewSet, basename='tour')

urlpatterns = [
    path(r'comments/', CommentAPI.as_view(), name='comment'),
] + router.urls
