from rest_framework import serializers
from .models import Itinerary, Comment, Like
from users.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Like
        fields = '__all__'


class ItinerarySerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)

    class Meta:
        model = Itinerary
        fields = ['id', 'name', 'is_public', 'created_at', 'updated_at', 'author', 'description', 'comments', 'likes']
