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
from django.core.paginator import Paginator
import requests
from django.conf import settings
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm

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
            user = authenticate(username=formulario.cleaned_data['username'], password=formulario.cleaned_data['password1'], request=request)
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
    paginator = Paginator(publicaciones, 8) # Muestra 10 obras por pagina
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    aux = {
        'page_obj' : page_obj
    }

    return render(request, 'core/colecciones.html', aux)

def coleccion_detalle(request, id):
    obra = get_object_or_404(Arte, id=id)
    return render(request, 'core/obra.html', {'obra': obra})

def artistas(request):
    biografia = Autor.objects.all()
    paginator = Paginator(biografia, 8) # Muestra 10 obras por pagina
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    aux = {
        'page_obj' : page_obj
    }

    return render(request, 'core/artistas.html', aux)

def artista_detalle(request, id):
    autor = get_object_or_404(Autor, id=id)
    return render(request, 'core/artista-detalle.html', {'autor': autor})

@login_required
def cart(request):
    cart_usuario, creado = Carrito.objects.get_or_create(usuario=request.user)

    cart = cart_usuario.items.all()

    total_cantidad = sum(item.cantidad for item in cart)

    subtotal = sum(item.subtotal() for item in cart)
    
    envio = 20
    
    total = subtotal + envio

    aux = {
        'cart': cart,
        'total_cantidad': total_cantidad,
        'subtotal': subtotal,
        'envio': envio,
        'total': total
    }

    return render(request, 'core/cart.html', aux)

@login_required
def add_cart(request, id):
    arte = get_object_or_404(Arte, id=id)
    usuario = request.user

    carrito, creado = Carrito.objects.get_or_create(usuario=usuario)

    if ItemCarrito.objects.filter(carrito=carrito, obra=arte).exists():
        itemCarrito = ItemCarrito.objects.get(carrito=carrito, obra=arte)
        itemCarrito.cantidad += 1
        itemCarrito.save()
        messages.success(request, f"{arte.titulo} se ha agregado al carrito.") 
    else:
        itemNuevo = ItemCarrito(carrito=carrito, obra=arte)
        itemNuevo.save()
        messages.success(request, f"{arte.titulo} se ha agregado al carrito.")
    
    return redirect('colecciones')

@login_required
def del_cart(request, id):
    item = get_object_or_404(ItemCarrito, id=id)
    arte = item.obra

    if item.carrito.usuario == request.user:
        if item.cantidad > 1:
            item.cantidad -= 1
            item.save()
            messages.success(request, f"Se elimino la cantidad de {arte.titulo} en el carrito.")
        else:
            item.delete()
            messages.success(request, f"{arte.titulo} se ha eliminado del carrito.")
    else:
        messages.error(request, "No tienes permisos para modificar este ítem del carrito.")

    return redirect('cart')

def account_locked(request):
    return render(request, 'core/account_locked.html')

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

@login_required
@permission_required('is_staff')
def adminsolicitud(request):
    publicaciones = Arte.objects.all()

    aux = {'obras': publicaciones}

    return render(request, 'core/admin/admin-solic.html',aux)

@login_required
@permission_required('is_staff')
def revision(request, id):
    obra = get_object_or_404(Arte, id=id)
    if request.method == 'POST':
        if 'aceptar' in request.POST:
            return redirect('aceptar_obra', id=obra.id)
        elif 'rechazar' in request.POST:
            return redirect('rechazar_obra', id=obra.id)

    return render(request, 'core/admin/revision.html', {'obra': obra})

@login_required
@permission_required('is_staff')
def aceptar_obra(request, id):
    obra = get_object_or_404(Arte, id=id)
    obra.habilitado = True
    obra.save()
    messages.success(request, 'Obra publicada en la página!')
    return render(request, 'core/admin/admin-solic.html')

@login_required
@permission_required('is_staff')
def rechazar_obra(request,id):
    obra = get_object_or_404(Arte, id=id)
    if request.method == 'POST':
        mensaje = request.POST.get('mensaje')
        obra.habilitado = False
        obra.mensaje = mensaje
        obra.save()
        messages.warning(request, 'Mensaje enviado al colaborador!')
        return redirect('adminsolicitud')
    return render(request, 'core/admin/rechazar-obra.html', {'obra': obra})



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
            return render(request, 'core/colab/colabgc.html')
        else:
            aux = {'form':formulario}
            messages.error(request, "No se pudo agregar el artista!")

    aux = {'form' : ArtistaCreationForm()}
    return render(request, 'core/colab/colab-autor.html', aux)

@login_required
@user_passes_test(lambda u: in_group(u, 'Colaborador'))
def colabadd(request):
    if request.method == 'POST':
        formulario = ArteCreationForm(request.POST, request.FILES, initial={'mensaje': ''})
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Solicitud creada correctamente!")
            return render(request, 'core/colab/colabgc.html')
        else:
            aux = {'form':formulario}
            messages.error(request, "No se pudo generar la solicitud!")

    aux = {'form' : ArteCreationForm()}
    return render(request, 'core/colab/colab-add.html', aux)

@login_required
@user_passes_test(lambda u: in_group(u, 'Colaborador'))
def colabupd(request, id):
    u = get_object_or_404(Arte, id=id)
    if request.method == 'POST':
        formulario = ArteCreationForm(data=request.POST, instance=u)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Obra Actualizada!")
            return redirect('colablist')
        else:
            messages.error(request, "No se pudo actualizar!")
    else:
        formulario = ArteCreationForm(instance=u)
            
            
    return render(request, 'core/colab/colab-upd.html', {'form': formulario})

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

##########################################################
##############      USER VIEWS       ####################
##########################################################

def configuracion(request, id):
    usuario = get_object_or_404(User, id=id)
    return render(request, 'core/user/user-config.html', {'usuario': usuario})

def userupd(request, id):
    usuario = get_object_or_404(User, id=id)
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST, instance=usuario)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data['username'], password=formulario.cleaned_data['password1'])
            login(request, user)
            messages.success(request, "Datos Actualizados Correctamente!")
            return redirect('index')
        else:
            messages.error(request, "No se pudo actualizar!")
    else:
        formulario = CustomUserCreationForm(instance=usuario)
            
            
    return render(request, 'core/user/user-upd.html', {'form': formulario})

# CONSUMO DE API
def ArteAPI(request):
    response = requests.get('http://127.0.0.1:8000/api/Arte/')
    arte = response.json()

    aux = {'obras' : arte}

    return render(request, 'core/crudapi/index.html', aux) 

