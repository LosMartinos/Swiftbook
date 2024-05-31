from rest_framework import generics
from django.contrib.auth.models import User
from .models import Anbieter, Dienstleistung, Buchung
from .serializers import UserSerializer, AnbieterSerializer, DienstleistungSerializer, BuchungSerializer

# List and create Users
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Retrieve, update, and delete a single User
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# List and create Anbieters
class AnbieterListCreateView(generics.ListCreateAPIView):
    queryset = Anbieter.objects.all()
    serializer_class = AnbieterSerializer

# Retrieve, update, and delete a single Anbieter
class AnbieterDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Anbieter.objects.all()
    serializer_class = AnbieterSerializer

# List and create Dienstleistungen
class DienstleistungListCreateView(generics.ListCreateAPIView):
    queryset = Dienstleistung.objects.all()
    serializer_class = DienstleistungSerializer

# Retrieve, update, and delete a single Dienstleistung
class DienstleistungDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dienstleistung.objects.all()
    serializer_class = DienstleistungSerializer

# List and create Buchungen
class BuchungListCreateView(generics.ListCreateAPIView):
    queryset = Buchung.objects.all()
    serializer_class = BuchungSerializer

# Retrieve, update, and delete a single Buchung
class BuchungDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Buchung.objects.all()
    serializer_class = BuchungSerializer
