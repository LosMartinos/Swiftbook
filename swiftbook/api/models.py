from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

class Provider(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    companyname = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phonenumber = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postalcode = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    longitude = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)

class Service(models.Model): 
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='dienstleistungen')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    length = models.DurationField()
    additional_fields = models.JSONField(default=list,blank=True, null=True)

class Booking(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    additional_data = models.JSONField(default=list,blank=True, null=True)

class BusinessHours(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    day = models.IntegerField()  # 0 = monday
    open_time = models.TimeField()
    close_time = models.TimeField()