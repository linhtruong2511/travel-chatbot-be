from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView

from .models import Users
from .serializers import UserSerializer
from rest_framework.decorators import action, api_view
from rest_framework import permissions

# Create your views here.
@api_view(['POST'])
def signup(request, *args, **kwargs):
    try:
        user = Users.objects.create_user(
            username=request.data.get('username'),
            email=request.data.get('email'),
            password=request.data.get('password'),
            first_name=request.data.get('first_name'),
            last_name=request.data.get('last_name'),
            phone=request.data.get('phone'),
            address=request.data.get('address'),
            age=request.data.get('age'),
        )
        print(user)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        print("Signup error:", e)
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class Info(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, format=None):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    def create(self, request, *args, **kwargs):
        user = Users.objects.create_user(
            username=request.data.get('username'),
            email=request.data.get('email'),
            password=request.data.get('password'),
            first_name=request.data.get('first_name'),
            last_name=request.data.get('last_name'),
            phone=request.data.get('phone'),
            address=request.data.get('address'),
            age=request.data.get('age'),
        )
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)