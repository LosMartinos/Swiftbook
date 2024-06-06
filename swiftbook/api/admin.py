from django.contrib import admin
from .models import Provider, Service, Booking, BusinessHours

# Register your models here.
admin.site.register(Provider)
admin.site.register(Service)
admin.site.register(Booking)
admin.site.register(BusinessHours)

