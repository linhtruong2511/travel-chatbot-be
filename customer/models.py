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

class Contact(models.Model):
    topic = models.CharField(max_length=100)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='contacts')
    message = models.TextField()
