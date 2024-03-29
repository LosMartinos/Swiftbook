from django.shortcuts import render
from rest_framework import generics
from .serializers import MyuserSerializer
from .models import Myuser
# Create your views here.
class MyuserView(generics.ListAPIView):
    queryset = Myuser.objects.all()
    serializer_class = MyuserSerializer