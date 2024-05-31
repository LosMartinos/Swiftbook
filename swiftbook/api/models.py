from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

class Anbieter(models.Model): #vlt erweiter dass man mehere dienstleistungen hat
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firmenname = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    telefonnummer = models.CharField(max_length=20, blank=True, null=True)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    stadt = models.CharField(max_length=100, blank=True, null=True)
    postleitzahl = models.CharField(max_length=20, blank=True, null=True)
    land = models.CharField(max_length=100, blank=True, null=True)
    oeffnungszeiten = models.JSONField(default=dict, blank=True, null=True)  #ändern? wie speichern? 
    logo = models.ImageField(upload_to='anbieter_logos/', blank=True, null=True)  #  Pillow library? Andere lib?

class Dienstleistung(models.Model): #Anbieter
    anbieter = models.ForeignKey(Anbieter, on_delete=models.CASCADE, related_name='dienstleistungen')
    name = models.CharField(max_length=255)
    beschreibung = models.TextField()
    dauer = models.DurationField() # // test oder filter, Schließzeit-Öffnungszeit / dauer = 0
    additional_fields = models.JSONField(default=list)

class Buchung(models.Model): #Kunden
    kunde = models.ForeignKey(User, on_delete=models.CASCADE)
    dienstleistung = models.ForeignKey(Dienstleistung, on_delete=models.CASCADE)
    startzeit = models.DateTimeField()
    endzeit = models.DateTimeField()
    additional_data = models.JSONField(default=list)



