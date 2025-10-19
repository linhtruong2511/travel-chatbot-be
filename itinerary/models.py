import uuid

from django.db import models

# Create your models here.
class Itinerary(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey('users.Users', null=True, on_delete=models.SET_NULL)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

# class Day(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     title = models.CharField(max_length=255)
#     itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name='days')
#     order = models.PositiveIntegerField(default=0)  # For sorting days
#
#     class Meta:
#         ordering = ['order']
#
#     def __str__(self):
#         return f"{self.title} (Itinerary: {self.itinerary.name})"
#
# class Activity(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     description = models.TextField()
#     day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name='activities')
#     order = models.PositiveIntegerField(default=0)  # For sorting activities
#
#     class Meta:
#         ordering = ['order']
#
#     def __str__(self):
#         return f"Activity in {self.day.title}"