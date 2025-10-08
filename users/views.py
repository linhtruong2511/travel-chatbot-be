from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Users
from .serializers import UserSerializer
from rest_framework.decorators import action, api_view
from rest_framework import permissions

# Create your views here.
@api_view(['POST'])
def signup(request, *args, **kwargs):
    try:
        print("User model:", Users)
        print("User manager:", getattr(Users, "objects", None))
        print("create_user exists:", hasattr(Users.objects, "create_user"))

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

class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )