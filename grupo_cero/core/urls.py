from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    	path('',index,name="index"),
        path('contacto/',contacto,name="contacto"),
        path('colecciones/',colecciones,name="colecciones"),
        path('artistas/',artistas,name="artistas"),
        path('coleccionessingle/',coleccionessingle,name="coleccionessingle"),
        path('artistasingle/',artistasingle,name="artistasingle"),
        path('admingc/',admingc,name="admingc"),
        path('adminadd/',adminadd,name="adminadd"),
        path('adminupd/',adminupd,name="adminupd"),
        path('adminlist/',adminlist,name="adminlist"),
        path('register/',register,name="register"),
        path('colabgc/',colabgc,name="colabgc"),
        path('colabadd/',colabadd,name="colabadd"),
        path('colabupd/',colabupd,name="colabupd"),
        path('colablist/',colablist,name="colablist"),
        path('artista2/',artistas2,name="artista2"),
	]

