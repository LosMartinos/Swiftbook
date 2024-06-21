from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Provider,Service,Booking, BusinessHours, Timeslot
from django.core.serializers import serialize

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    provider = ProviderSerializer()  # Include related Provider
    class Meta:
        model = Service
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()  # Include related Service
    class Meta:
        model = Booking
        fields = '__all__'

class BusinessHoursSerializer(serializers.ModelSerializer):
    provider = ProviderSerializer()  # Include related Provider
    class Meta:
        model = BusinessHours
        fields = '__all__'

class TimeslotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeslot
        fields = '__all__'
