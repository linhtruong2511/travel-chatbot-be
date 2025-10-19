from rest_framework import serializers
from .models import Itinerary
from users.serializers import UserSerializer


# class ActivitySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Activity
#         fields = ['id', 'description', 'order' ]
#
# class DaySerializer(serializers.ModelSerializer):
#     activities = ActivitySerializer(many=True)
#
#     class Meta:
#         model = Day
#         fields = ['id', 'title', 'activities', 'order']

    # def create(self, validated_data):
    #     activities_data = validated_data.pop('activities', [])
    #     day = Day.objects.create(**validated_data)
    #     for activity_data in activities_data:
    #         Activity.objects.create(day=day, **activity_data)
    #     return day
    #
    # def update(self, instance, validated_data):
    #     activities_data = validated_data.pop('activities', [])
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.order = validated_data.get('order', instance.order)
    #     instance.save()
    #
    #     # Update activities (simple: delete all and recreate; optimize if needed)
    #     instance.activities.all().delete()
    #     for activity_data in activities_data:
    #         Activity.objects.create(day=instance, **activity_data)
    #     return instance


class ItinerarySerializer(serializers.ModelSerializer):
    # days = DaySerializer(many=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Itinerary
        fields = ['id', 'name', 'is_public', 'created_at', 'updated_at', 'author', 'description']

    # def create(self, validated_data):
    #     days_data = validated_data.pop('days', [])
    #     itinerary = Itinerary.objects.create(**validated_data)
    #     for day_data in days_data:
    #         DaySerializer().create({**day_data, 'itinerary': itinerary})
    #     return itinerary
    #
    # def update(self, instance, validated_data):
    #     days_data = validated_data.pop('days', [])
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.is_public = validated_data.get('is_public', instance.is_public)
    #     instance.save()
    #
    #     # Update days (simple: delete all and recreate; optimize if needed)
    #     instance.days.all().delete()
    #     for day_data in days_data:
    #         DaySerializer().create({**day_data, 'itinerary': instance})
    #     return instance