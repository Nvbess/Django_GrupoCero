from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
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
from django.http import JsonResponse
import random
import json
import requests
import cloudinary
import cloudinary.uploader
import cloudinary.api
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template,render_to_string 
from xhtml2pdf import pisa
from django.contrib.auth.views import (PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView,)
from django.urls import reverse_lazy
from .forms import ResetPasswordForm, NewPasswordForm
import os

class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/reset_password.html'
    email_template_name = 'registration/password_reset_email.html'
    form_class = ResetPasswordForm
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/reset_password_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/reset_password_confirm.html'
    form_class = NewPasswordForm
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/reset_password_complete.html'

# Configurar Cloudinary con tus credenciales
cloudinary.config(
    cloud_name= os.getenv('CLOUDINARY_NAME'),
    api_key= os.getenv('CLOUDINARY_API_KEY'),
    api_secret= os.getenv('CLOUDINARY_API_SECRET')
)

def in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

def IndicadorAPI():
    try:
        response = requests.get('https://mindicador.cl/api')
        data = response.json()
        usd_rate = data['dolar']['valor']
        return usd_rate
    except Exception as e:
        print("Error al obtener la tasa de cambio:", e)
        return None

def ObtenerDetalleMET(object_id):
    base_url = "https://collectionapi.metmuseum.org/public/collection/v1/objects/"
    url = f"{base_url}{object_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        artwork_details = {
            'title': data.get('title'),
            'artist': data.get('artistDisplayName'),
            'image': ObtenerImagenMET(data),
            'bio': data.get('artistDisplayBio'),
            'pais': data.get('artistNationality')
        }
        if artwork_details['image'] and artwork_details['artist'] and artwork_details['bio']:
            return artwork_details
    return None

def ObtenerImagenMET(data):
    if 'primaryImage' in data:
        return data['primaryImage']
    elif 'images' in data and len(data['images']) > 0:
        return data['images'][0]['baseimageurl']
    else:
        return 'No se encontro la imagen'

def RandomMET(request):
    base_url = "https://collectionapi.metmuseum.org/public/collection/v1/search"
    params = {
        'q': 'paintings',  # Filtrar por pinturas
        'medium': 'Paintings'
    }
    response = requests.get(base_url, params=params)

    artworks = []
    if response.status_code == 200:
        data = response.json()
        object_ids = data.get('objectIDs', [])
        if object_ids:
            valid_artworks = []
            while len(valid_artworks) < 3 and object_ids:
                random_id = random.choice(object_ids)
                object_ids.remove(random_id)
                artwork = ObtenerDetalleMET(random_id)
                if artwork:
                    valid_artworks.append(artwork)
            artworks = valid_artworks

    return render(request, 'core/crudapi/artworks.html', {'artworks': artworks})

##########################################################
##############      VIEWS PRINCIPAL   ####################
##########################################################

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
    paginator = Paginator(publicaciones, 8) # Muestra 8 obras por pagina
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    aux = {
        'page_obj': page_obj
    }

    return render(request, 'core/colecciones.html', aux)

def coleccion_detalle(request, id):
    obra = get_object_or_404(Arte, id=id)
    usd_rate = IndicadorAPI()
    obra_usd_price = obra.valor * usd_rate if usd_rate else None

    return render(request, 'core/obra.html', {
        'obra': obra,
        'usd_rate': usd_rate,
        'obra_usd_price': obra_usd_price
    })

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

def account_locked(request):
    return render(request, 'core/account_locked.html')

@login_required
def cart(request):
    cart_usuario, creado = Carrito.objects.get_or_create(usuario=request.user)

    cart = cart_usuario.items.all()

    total_cantidad = sum(item.cantidad for item in cart)
    subtotal = sum(item.subtotal() for item in cart)
    envio = 10
    total = subtotal + envio

    usd_rate = IndicadorAPI()

    # Calcular los valores en USD
    if usd_rate:
        cart_with_usd = [(item, item.subtotal() * usd_rate) for item in cart]
        subtotal_usd = subtotal * usd_rate
        envio_usd = envio * usd_rate
        total_usd = total * usd_rate
    else:
        cart_with_usd = [(item, None) for item in cart]
        subtotal_usd = None
        envio_usd = None
        total_usd = None

    aux = {
        'cart': cart_with_usd,
        'total_cantidad': total_cantidad,
        'subtotal': subtotal,
        'subtotal_usd': subtotal_usd,
        'envio': envio,
        'envio_usd': envio_usd,
        'total': total,
        'total_usd': total_usd
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

@csrf_exempt
@login_required
def payment_confirmation(request, voucher_id=None):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            voucher = VoucherCompra.objects.create(
                usuario=request.user,
                payment_id=data['paymentID'],
                payer_id=data['payerID'],
                order_id=data['orderID'],
                payment_token=data['paymentToken'],
                return_url=data['returnUrl'],
                details=data['details'],
            )
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

        return JsonResponse({'voucher_id': voucher.id})

    if voucher_id:
        voucher = get_object_or_404(VoucherCompra, id=voucher_id)
        if voucher.usuario != request.user:
            return JsonResponse({'error': 'No tienes permiso para ver este voucher.'}, status=403)
        return render(request, 'core/payment/voucher.html', {'voucher': voucher})
    else:
        return JsonResponse({'error': 'Voucher ID not provided'}, status=400)

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

# UTILIZAMOS LOS VIEWSETS PARA MANEJAR LAS SOLICITUDES HTTP (GET,POST,PUT,DELETE)
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


##########################################################
##############      USER VIEWS       ####################
##########################################################

def configuracion(request, id):
    usuario = get_object_or_404(User, id=id)
    vouchers = VoucherCompra.objects.filter(usuario=usuario)
    return render(request, 'core/user/user-config.html', {'usuario': usuario, 'vouchers': vouchers})

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

##########################################################
##############      PDF       ####################
##########################################################

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

@login_required
def generate_voucher_pdf(request, voucher_id):
    voucher = get_object_or_404(VoucherCompra, id=voucher_id)
    
    if voucher.usuario != request.user:
        return HttpResponse("Acceso denegado para este voucher.", status=403)
    
    html = render_to_string('core/payment/voucher-pdf.html', {'voucher': voucher})
    
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="voucher_{voucher.payment_id}.pdf"'
        return response
    
    return HttpResponse('Error al generar el PDF.', status=500)


