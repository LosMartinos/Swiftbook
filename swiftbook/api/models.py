from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Myuser(models.Model):
    surname = models.CharField(max_length=50)
    birthdate = models.DateField()


