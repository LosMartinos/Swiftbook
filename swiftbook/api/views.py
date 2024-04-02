from django.shortcuts import render
from rest_framework import generics
from .serializers import MyUserSerializer
from .models import MyUser
# Create your views here.

class MyUserView(generics.CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer