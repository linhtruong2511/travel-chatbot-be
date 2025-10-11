from django.db import models


# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    zalo = models.CharField(max_length=100, null=True)
    facebook = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    age = models.IntegerField(null=True)


class Contact(models.Model):
    topic = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    zalo = models.CharField(max_length=100, null=True, blank=True)
    facebook = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    message = models.TextField(blank=True)
