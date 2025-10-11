from rest_framework import serializers
from .models import Users

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Users
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone',
            'address',
            'age',
            'phone',
            'date_joined',
            'is_active',
            'is_staff',
            'is_superuser',
        ]
