from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import Group,User
from rest_framework import viewsets
from .serializers import *
from rest_framework.renderers import JSONRenderer
import requests

def in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

# Create your views here.
def index(request):
    return render(request, 'core/index.html')

def register(request):
    aux = {
        'form' : CustomUserCreationForm()
    }
    
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            user = formulario.save()
            # AÑADIMOS EL GRUPO CLIENTE AL USUARIO
            group = Group.objects.get(name='Usuario')
            user.groups.add(group)
            # Autenticamos al user y lo redireccionamos
            user = authenticate(username=formulario.cleaned_data['username'], password=formulario.cleaned_data['password1'])
            login(request, user)
            messages.success(request, "Registro Completado Correctamente!")
            # Redirecciona
            return redirect(to="index")
        else:
            aux['form'] = formulario
            messages.error(request, "No se pudo registrar!")
            
    return render(request, 'registration/register.html', aux)

def contacto(request):
    return render(request, 'core/contacto.html')

def colecciones(request):
    publicaciones = Arte.objects.all()
    aux = {'obras': publicaciones}
    return render(request, 'core/colecciones.html', aux)

def coleccion_detalle(request, id):
    obra = get_object_or_404(Arte, id=id)
    return render(request, 'core/obra.html', {'obra': obra})

def artistas(request):
    biografia = Autor.objects.all()

    aux = {'autor': biografia}

    return render(request, 'core/artistas.html', aux)

def artista_detalle(request, id):
    autor = get_object_or_404(Autor, id=id)
    return render(request, 'core/artista-detalle.html', {'autor': autor})

##########################################################
##############      ADMIN VIEWS       ####################
##########################################################

@login_required 
@permission_required('is_staff')
def admingc(request):
	return render(request, 'core/admin/admingc.html')

@login_required
@permission_required('is_staff')
def adminadd(request):
    aux = {
        'form' : ColabCreationForm()
    }
    
    if request.method == 'POST':
        formulario = ColabCreationForm(data=request.POST)
        if formulario.is_valid():
            user = formulario.save()
            # AÑADIMOS EL GRUPO CLIENTE AL USUARIO
            group = Group.objects.get(name='Colaborador')
            user.groups.add(group)
            messages.success(request, "Colaborador Agregado Correctamente!")
        else:
            aux['form'] = formulario
            messages.error(request, "No se pudo registrar al colaborador!")
            
    return render(request, 'core/admin/admin-add.html', aux)

@login_required
@permission_required('is_staff')
def adminlist(request):
    # Obtener el grupo "Colaborador"
    grupo_colaboradores = Group.objects.get(name='Colaborador')
    # Obtener los usuarios que pertenecen a este grupo
    colaboradores = User.objects.filter(groups=grupo_colaboradores).values('first_name','last_name','username', 'email')
    context = {'colaboradores': colaboradores}
    return render(request, 'core/admin/admin-list.html', context)

@login_required
@permission_required('is_staff')
def admindel(request, username):    
    try:
        u = User.objects.get(username = username)
        u.delete()
        messages.success(request, "Colaborador Eliminado!")
    except:
      messages.error(request, "Usuario no encontrado!")    
    return redirect('adminlist') 

@login_required
@permission_required('is_staff')
def adminupd(request, username):
    u = get_object_or_404(User, username=username)
    if request.method == 'POST':
        formulario = ColabCreationForm(data=request.POST, instance=u)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Colaborador Actualizado!")
            return redirect('adminlist')
        else:
            messages.error(request, "No se pudo actualizar!")
    else:
        formulario = ColabCreationForm(instance=u)
            
            
    return render(request, 'core/admin/admin-upd.html', {'form': formulario})

##########################################################
##############      COLABORADOR VIEWS       ##############
##########################################################

@login_required
@user_passes_test(lambda u: in_group(u, 'Colaborador'))
def colabgc(request):
    return render(request, 'core/colab/colabgc.html')

@login_required
@user_passes_test(lambda u: in_group(u, 'Colaborador'))
def colabautor(request):
    if request.method == 'POST':
        formulario = ArtistaCreationForm(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Artista agregado exitosamente!")
        else:
            aux = {'form':formulario}
            messages.error(request, "No se pudo agregar el artista!")

    aux = {'form' : ArtistaCreationForm()}
    return render(request, 'core/colab/colab-autor.html', aux)

@login_required
@user_passes_test(lambda u: in_group(u, 'Colaborador'))
def colabadd(request):
    if request.method == 'POST':
        formulario = ArteCreationForm(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Obra agregada exitosamente!")
        else:
            aux = {'form':formulario}
            messages.error(request, "No se pudo agregar la obra!")

    aux = {'form' : ArteCreationForm()}
    return render(request, 'core/colab/colab-add.html', aux)

@login_required
@user_passes_test(lambda u: in_group(u, 'Colaborador'))
def colabupd(request):
    return render(request, 'core/colab/colab-upd.html')

@login_required
@user_passes_test(lambda u: in_group(u, 'Colaborador'))
def colablist(request):
    publicaciones = Arte.objects.all()

    aux = {'obras': publicaciones}
    return render(request, 'core/colab/colab-list.html', aux)

##########################################################
##############      SECCION DE APIS         ##############
##########################################################


#UTILIZAMOS LOS VIEWSETS PARA MANEJAR LAS SOLICITUDES HTTP (GET,POST,PUT,DELETE)
class ArteViewset(viewsets.ModelViewSet):
    queryset = Arte.objects.all()
    serializer_class = ArteSerializer
    renderer_classes = [JSONRenderer]

class AutorViewset(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    renderer_classes = [JSONRenderer]

# CONSUMO DE API
def ArteAPI(request):
    response = requests.get('http://127.0.0.1:8000/api/Arte/')
    arte = response.json()

    aux = {'obras' : arte}

    return render(request, 'core/crudapi/index.html', aux) 

