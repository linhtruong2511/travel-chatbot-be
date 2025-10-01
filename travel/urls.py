from django.urls import path
from .views import TourViewSet
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'tours', TourViewSet, basename='tour')

urlpatterns = [
] + router.urls
