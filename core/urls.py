from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

# CONFIGURACION API
router = routers.DefaultRouter()
router.register('Arte', ArteViewset)
router.register('Autor', AutorViewset)

urlpatterns = [
    	path('',index,name="index"),
        path('contacto/',contacto,name="contacto"),
        path('colecciones/',colecciones,name="colecciones"),
        path('obra/<int:id>/',coleccion_detalle,name="coleccion_detalle"),
        path('artistas/',artistas,name="artistas"),
        path('artista/<int:id>/',artista_detalle,name="artista_detalle"),
        path('admingc/',admingc,name="admingc"),
        path('adminadd/',adminadd,name="adminadd"),
        path('adminlist/',adminlist,name="adminlist"),
        path('aceptar_obra/<int:id>/', aceptar_obra, name='aceptar_obra'),
        path('rechazar_obra/<int:id>/',rechazar_obra, name='rechazar_obra'),
        path('adminsolicitud/',adminsolicitud,name="adminsolicitud"),
        path('adminlist/delete/<str:username>/',admindel,name="admindel"),
        path('adminlist/update/<str:username>/',adminupd,name="adminupd"),
        path('register/',register,name="register"),
        path('colabgc/',colabgc,name="colabgc"),
        path('colabadd/',colabadd,name="colabadd"),
        path('colabupd/<int:id>',colabupd,name="colabupd"),
        path('colablist/',colablist,name="colablist"),
        path('colabautor/',colabautor,name="colabautor"),
        path('configuracion/<int:id>/',configuracion,name="configuracion"),
        path('userupd/<int:id>/',userupd,name="userupd"),
        path('cart/', cart, name="cart"),
        path('revision/<int:id>/', revision, name="revision"),
        path('account_locked/', account_locked, name="account_locked"),
        path('add_cart/<int:id>/', add_cart, name="add_cart"),
        path('del_cart/<int:id>/', del_cart, name="del_cart"),
        # Voucher
        path('confirmacion/', payment_confirmation, name='confirmacion'),
        path('confirmacion/<int:voucher_id>/', payment_confirmation, name='voucher'),
        path('voucher-pdf/<int:voucher_id>/', generate_voucher_pdf, name='voucher_pdf'),
        # API
        path('api/', include(router.urls)),
        path('arte', ArteAPI, name='arte'),
	]

