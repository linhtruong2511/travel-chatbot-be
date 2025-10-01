from django.urls import path
from .views import Chatbot

urlpatterns = [
    path('', Chatbot.as_view(), name='chatbot'),
]