from django.db import models


class Tour(models.Model):
    name = models.TextField(max_length=255)
    duration = models.IntegerField(default=0, blank=True)
    duration_detail = models.TextField(default="", blank=True)
    min_budget = models.IntegerField(default=0)
    max_budget = models.IntegerField(default=0)
    budget_detail = models.TextField(default="")
    budget_current = models.TextField(default="")
    rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    tags = models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to="tours/", null=True, blank=True)
    location = models.CharField(max_length=500, default="")
    numberOfPeople = models.CharField(default="", max_length=100, blank=True)
    difficulty = models.CharField(max_length=125, default="", blank=True)
    thumbnail_url = models.TextField(default="", blank=True)
    short_description = models.TextField(default="", blank=True)
    highlights = models.TextField(default="", blank=True)

    class Meta:
        ordering = ['id']


class Description(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='descriptions')
    text = models.TextField()

class Note(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='notes')
    text = models.TextField()

class TourImages(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="tours/")