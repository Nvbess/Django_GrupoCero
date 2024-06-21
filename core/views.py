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
from django.conf import settings
import json
import requests
import cloudinary
import cloudinary.uploader
import cloudinary.api
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template,render_to_string 
from xhtml2pdf import pisa



# Configurar Cloudinary con tus credenciales
cloudinary.config(
    cloud_name="dyh1syxfx",
    api_key="346192587839451",
    api_secret="l6A_FW9Xm4zY8yJrpPVU7B7IgoA"
)

def in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

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

def account_locked(request):
    return render(request, 'core/account_locked.html')

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

@csrf_exempt
@login_required
def payment_confirmation(request, voucher_id=None):
    if request.method == 'POST':
        data = json.loads(request.body)
        voucher = Voucher.objects.create(
            usuario= request.user,
            payment_id=data['paymentID'],
            payer_id=data['payerID'],
            order_id=data['orderID'],
            payment_token=data['paymentToken'],
            return_url=data['returnUrl'],
            details=data['details'],
        )
        return JsonResponse({'voucher_id': voucher.id})
    
    if voucher_id:
        voucher = get_object_or_404(Voucher, id=voucher_id)
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

def obtener_token():
    url = "https://api.artsy.net/api/tokens/xapp_token"
    data = {
        "client_id": settings.ARTSY_CLIENT_ID,
        "client_secret": settings.ARTSY_CLIENT_SECRET
    }
    response = requests.post(url, data=data)
    return response.json().get('token')

def obtener_obras(token):
    headers = {
        "X-Xapp-Token": token
    }
    url = "https://api.artsy.net/api/artworks"
    response = requests.get(url, headers=headers)
    obras = response.json().get('_embedded', {}).get('artworks', [])
    # Transformar los datos para que las claves sean compatibles con Django
    for obra in obras:
        obra['links'] = obra.pop('_links')
        # Verifica si 'image_versions' y 'image' están presentes
        if 'image_versions' in obra['links']['image'] and 'href' in obra['links']['image']:
            image_url = obra['links']['image']['href']
            if '{image_version}' in image_url:
                image_url = image_url.replace('{image_version}', 'large')
            obra['imagen_url'] = image_url
        else:
            obra['imagen_url'] = ''
    return obras

def ExhibicionAPI(request):
    token = obtener_token()
    obras = obtener_obras(token)
    contexto = {
        'obras': obras
    }
    return render(request, 'core/crudapi/exhibicion.html', contexto)

##########################################################
##############      USER VIEWS       ####################
##########################################################

def configuracion(request, id):
    usuario = get_object_or_404(User, id=id)
    vouchers = Voucher.objects.filter(usuario=usuario)
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
    # Obtener el voucher por su ID
    voucher = get_object_or_404(Voucher, id=voucher_id)
    
    # Verificar que el voucher pertenezca al usuario autenticado
    if voucher.usuario != request.user:
        return HttpResponse("Acceso denegado para este voucher.", status=403)
    
    # Renderizar la plantilla HTML a una cadena de texto HTML
    html = render_to_string('core/payment/voucher-pdf.html', {'voucher': voucher})
    
    # Crear un archivo en memoria (BytesIO) para el PDF
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
    # Si se generó correctamente el PDF, devolverlo como una respuesta de Django
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="voucher_{voucher.payment_id}.pdf"'
        return response
    
    # Si hubo algún error al generar el PDF, devolver un mensaje de error
    return HttpResponse('Error al generar el PDF.', status=500)


