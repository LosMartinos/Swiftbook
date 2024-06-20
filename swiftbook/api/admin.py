from django.contrib import admin
from .models import *
from django.contrib.sessions.models import Session


# Register your models here.
admin.site.register(Provider)
admin.site.register(Service)
admin.site.register(Booking)
admin.site.register(BusinessHours)
admin.site.register(Session)
admin.site.register(Timeslot)

