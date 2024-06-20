from rest_framework import serializers
from .models import *

# LO UTILIZAMOS PARA TRANSFORMAR PYTHON A JSON
class ArteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arte
        fields = '__all__'

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'