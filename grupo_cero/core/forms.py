from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from django_recaptcha.fields import ReCaptchaField

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','email', 'password1', 'password2']
        help_texts = {
            'username': None
        }
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este usuario ya existe!")
        return username

class ColabCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','email', 'password1', 'password2']
        help_texts = {
            'username': None,
            'password1': None
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este usuario ya existe!")
        return username

class ArteCreationForm(forms.ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = Arte
        fields = ['titulo','autor','descripcion','valor','imagen','categoria','mensaje']

    mensaje = forms.CharField(required=False, widget=forms.HiddenInput())

class ArtistaCreationForm(forms.ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model =  Autor
        fields = ['nombre','descripcion','imagen']

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['nombre', 'apellido', 'rut', 'telefono', 'direccion', 'ciudad']

        


