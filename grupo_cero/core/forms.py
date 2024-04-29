from django import forms
from django.forms import ModelForm
from .models import *

class ObraForm(ModelForm):
    class Meta:
        model = Obra
        # fields = ['autor','descripcion','nombre_obra'] <--- Forma individual
        fields = '__all__'

class TipoObraForm(ModelForm):
    class Meta:
        model = TipoObra
        # fields = ['descripcion'] <--- Forma individual celda x celda
        fields = '__all__'