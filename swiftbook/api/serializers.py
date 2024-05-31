from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Anbieter, Dienstleistung, Buchung

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class AnbieterSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Anbieter
        fields = ['id', 'user', 'firmenname', 'email', 'telefonnummer', 'adresse', 'stadt', 'postleitzahl', 'land']

class DienstleistungSerializer(serializers.ModelSerializer):
    anbieter = AnbieterSerializer()

    class Meta:
        model = Dienstleistung
        fields = ['id', 'anbieter', 'name', 'beschreibung', 'dauer', 'additional_fields']

class BuchungSerializer(serializers.ModelSerializer):
    kunde = UserSerializer()
    dienstleistung = DienstleistungSerializer()

    class Meta:
        model = Buchung
        fields = ['id', 'kunde', 'dienstleistung', 'startzeit', 'endzeit', 'additional_data']
