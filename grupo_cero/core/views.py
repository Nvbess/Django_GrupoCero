from django.shortcuts import render, redirect
from .models import *
from .forms import *


# Create your views here.
def index(request):
    return render(request, 'core/index.html')

def contacto(request):
    return render(request, 'core/contacto.html')

def colecciones(request):
    return render(request, 'core/colecciones.html')

def artistas(request):
    return render(request, 'core/artistas.html')

def artistauno(request):
    return render(request, 'core/artista-single.html')

def coleccionessingle(request):
    return render(request, 'core/coleccionessingle.html')

def admingc(request):
	return render(request, 'core/admin/admingc.html')

#def obrasadd(request):
		#aux = {
		#	'form' : ObraForm()
		#}

		#if request.method == 'POST':
		#	formulario = ObraForm(request.POST)
		#	if formulario.is_valid():
		#		formulario.save()
		#		aux['msj'] = "Empleado guardado correctamente!"
		#	else:
		#		aux['form'] = formulario

		#return render(request, 'core/obras/crud/add.html', aux)
    		

#def obrasupd(request, id):
		
		#obra = Obra.objects.get(id=id)
		#aux = {
		#	'form' : ObraForm(instance=obra)
		#}
		#if request.method == 'POST':
		#	formulario = ObraForm(request.POST, instance=obra)
		#	if formulario.is_valid():
		#		formulario.save()
		#		aux['msj'] = "Empleado modificado correctamente!"
		#		aux['form'] = formulario
		#		
#
#		return render(request, 'core/obras/crud/actualizar.html', aux)

#def obras(request):
		#obras = Obra.objects.all()
		#aux = {
		#	'lista' : obras
		#}

		#return render(request, 'core/obras/obras.html', aux)