from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import Group,User
from django.contrib import messages

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
            # Redirecciona
            return redirect(to="index")
        else:
            aux['form'] = formulario
            
    return render(request, 'registration/register.html', aux)


def contacto(request):
    return render(request, 'core/contacto.html')

def colecciones(request):
    return render(request, 'core/colecciones.html')

def artistas(request):
    return render(request, 'core/artistas.html')

def artistasingle(request):
    return render(request, 'core/artista-single.html')

def coleccionessingle(request):
    return render(request, 'core/coleccionessingle.html')

def artistas2(request):
    	return render(request, 'core/artistas-alt.html')

# ADMIN VIEWS

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
            # Redirecciona
            return redirect(to="admingc")
        else:
            aux['form'] = formulario
            
    return render(request, 'core/admin/admin-add.html', aux)

@login_required
@permission_required('is_staff')
def adminlist(request):
    # Obtener el grupo "Colaborador"
    grupo_colaboradores = Group.objects.get(name='Colaborador')
    # Obtener los usuarios que pertenecen a este grupo
    colaboradores = User.objects.filter(groups=grupo_colaboradores).values('username', 'email')
    context = {
        'colaboradores': colaboradores
    }
    return render(request, 'core/admin/admin-list.html', context)

@login_required
@permission_required('is_staff')
def admindel(request, username):    
    try:
        u = User.objects.get(username = username)
        u.delete()
        messages.sucess(request, "The user is deleted")
    except:
      messages.error(request, "The user not found")    
    return redirect('adminlist') 

def adminupd(request):
    return render(request, 'core/admin/admin-list.html')


# COLABORADOR VIEWS

def colabgc(request):
    return render(request, 'core/colab/colabgc.html')

def colabadd(request):
    aux = {
        'form' : ArteCreationForm()
    }

    if request.method == 'POST':
        formulario = ArteCreationForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
        else:
            aux['form'] = formulario

    return render(request, 'core/colab/colab-add.html', aux)

def colabupd(request):
    return render(request, 'core/colab/colab-upd.html')

def colablist(request):
    solicitudes = Arte.objects.all()

    aux = {
        'solicitudes': solicitudes
    }
    return render(request, 'core/colab/colab-list.html', aux)





             
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




