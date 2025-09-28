from django.db import models


class Tour(models.Model):
    name = models.TextField(max_length=255)
    duration = models.IntegerField(default=0)
    duration_detail = models.TextField(default="")
    min_budget = models.IntegerField(default=0)
    max_budget = models.IntegerField(default=0)
    budget_detail = models.TextField(default="")
    budget_current = models.TextField(default="")
    rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    description = models.TextField(default="")
    note = models.TextField(default="")
    tags = models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to="tours/", null=True, blank=True)
    
    def __str__(self):
        return self.name

class ToursImage(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="tours/")