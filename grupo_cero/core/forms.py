from django import forms
from django.forms import ModelForm
from .models import *

class ColaboradorForm(ModelForm):

    class Meta:
        model = Colaborador
        fields = '__all__'
