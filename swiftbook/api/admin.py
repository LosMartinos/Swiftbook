from django.contrib import admin
from .models import *
from django.contrib.sessions.models import Session


# Register your models here.

from django.contrib import admin
from .models import Service, Booking, BusinessHours, Timeslot, Provider
from django.contrib.sessions.models import Session

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'email', 'phonenumber', 'address', 'city', 'postalcode', 'country', 'longitude', 'latitude')
    search_fields = ('user__username', 'name', 'email', 'phonenumber', 'address', 'city', 'postalcode', 'country', 'longitude', 'latitude')
    list_filter = ('city', 'country')

    def username(self, obj):
        return obj.user.username
    username.short_description = 'Username'

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider_username', 'description', 'length', 'additional_fields')
    search_fields = ('name', 'provider__user__username', 'description', 'additional_fields')
    list_filter = ('name','provider__user__username')

    def provider_username(self, obj):
        return obj.provider.user.username
    provider_username.short_description = 'Provider Username'

@admin.register(BusinessHours)
class BusinessHoursAdmin(admin.ModelAdmin):
    list_display = ('provider_username', 'get_day_display', 'open_time', 'close_time')
    list_filter = ('provider__user__username', 'day')

    def get_day_display(self, obj):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        return days[obj.day]
    get_day_display.short_description = 'Day'

    def provider_username(self, obj):
        return obj.provider.user.username

@admin.register(Timeslot)
class TimeslotAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'date', 'time', 'booked_by')
    list_filter = ('service__provider__user__username', 'date')
    search_fields = ('service__name', 'service__provider__user__username', 'booked_by__username')

    def provider_username(self, obj):
        return obj.provider.user.username
    
    def service_name(self, obj):
        return obj.service.name
    
@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'session_data', 'expire_date')
