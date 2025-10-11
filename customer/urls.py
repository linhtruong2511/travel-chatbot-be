from rest_framework.urls import urlpatterns
from rest_framework import routers
from .views import ContactViewSet, CustomerViewSet

router = routers.DefaultRouter()
router.register('contacts', ContactViewSet)
router.register('', CustomerViewSet)

urlpatterns = [

] + router.urls