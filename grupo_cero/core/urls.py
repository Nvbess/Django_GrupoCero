from django.urls import path
from .views import *


urlpatterns = [
    	path('',index,name="index"),
        path('contacto/',contacto,name="contacto"),
        path('colecciones/',colecciones,name="colecciones"),
        path('artistas/',artistas,name="artistas"),
        path('coleccionessingle/',coleccionessingle,name="coleccionessingle"),
        path('artistauno/',artistauno,name="artistauno"),
        path('admingc/',admingc,name="admin"),
        path('admin/admin-add/',adminadd,name="admin-add"),
        path('admin/admin-upd/',adminupd,name="admin-upd"),
        path('admin/admin-list/',adminlistar,name="admin-list"),
	]