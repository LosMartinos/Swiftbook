from rest_framework import serializers
from .models import Myuser

class MyuserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Myuser
        fields = '__all__'