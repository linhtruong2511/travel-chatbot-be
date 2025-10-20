import uuid

from django.db import models

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

class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey('users.Users', null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    itinerary = models.ForeignKey('Itinerary', related_name='likes', null=True, on_delete=models.SET_NULL)

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey('users.Users', null=True, on_delete=models.SET_NULL)
    itinerary = models.ForeignKey('Itinerary', null=True, on_delete=models.SET_NULL, related_name='comments')
    def __str__(self):
        return self.content
