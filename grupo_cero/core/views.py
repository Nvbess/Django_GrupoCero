from django.shortcuts import render
from .models import *

# Create your views here.

def index(request):
    	return render(request, 'core/index.html')

def contacto(request):
    	return render(request, 'core/contacto.html')

def colecciones(request):
    	return render(request, 'core/colecciones.html')

def artistas(request):
    	return render(request, 'core/artistas.html')

def obras(request):
		obras = Obra.objects.all()
		aux = {
			'lista' : obras
		}

		return render(request, 'core/obras/obras.html', aux)