from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Users(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=11, null=True)
    address = models.CharField(max_length=100, null=True)
    age = models.IntegerField(null=True)

