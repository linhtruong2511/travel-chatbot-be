from rest_framework import serializers
from .models import Tour, TourImages, Description, Note, Comment


class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = '__all__'
        extra_kwargs = {"tour": {"read_only": True}}

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'
        extra_kwargs = {"tour": {"read_only": True}}
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class TourSerializer(serializers.ModelSerializer):
    descriptions = DescriptionSerializer(many=True)
    notes = NoteSerializer(many=True)
    comments = CommentSerializer(many=True)

    class Meta:
        model = Tour
        fields = '__all__'

    def create(self, validated_data):
        descriptions_data = validated_data.pop('descriptions', [])
        notes_data = validated_data.pop('notes', [])
        tour = Tour.objects.create(**validated_data)

        for desc in descriptions_data:
            Description.objects.create(tour=tour, **desc)
        for note in notes_data:
            Note.objects.create(tour=tour, **note)

        return tour

    def update(self, instance, validated_data):
        # Pop nested data
        descriptions_data = validated_data.pop('descriptions', [])
        notes_data = validated_data.pop('notes', [])

        # Update fields của tour
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Replace toàn bộ descriptions
        instance.descriptions.all().delete()
        for desc in descriptions_data:
            Description.objects.create(tour=instance, **desc)

        # Replace toàn bộ notes
        instance.notes.all().delete()
        for note in notes_data:
            Note.objects.create(tour=instance, **note)

        return instance


