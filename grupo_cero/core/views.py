from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import Group,User


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

def artistas(request):
    return render(request, 'core/artistas.html')

def artistasingle(request):
    return render(request, 'core/artista-single.html')

def coleccion_detalle(request, id):
    obra = get_object_or_404(Arte, id=id)
    return render(request, 'core/obra.html', {'obra': obra})

def artistas2(request):
    	return render(request, 'core/artistas-alt.html')

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

def colabgc(request):
    return render(request, 'core/colab/colabgc.html')

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

def colabupd(request):
    return render(request, 'core/colab/colab-upd.html')

def colablist(request):
    publicaciones = Arte.objects.all()

    aux = {'obras': publicaciones}
    return render(request, 'core/colab/colab-list.html', aux)