from django.urls import path
from .views import TourViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tours', TourViewSet, basename='tour')

urlpatterns = [
] + router.urls
