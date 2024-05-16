from django.urls import path
from .views import *


urlpatterns = [
    	path('',index,name="index"),
        path('contacto/',contacto,name="contacto"),
        path('colecciones/',colecciones,name="colecciones"),
        path('artistas/',artistas,name="artistas"),
        path('coleccionessingle/',coleccionessingle,name="coleccionessingle"),
        path('artistauno/',artistauno,name="artistauno"),
        path('admingc/',admingc,name="admingc"),
        path('adminadd/',adminadd,name="adminadd"),
        path('adminupd/',adminupd,name="adminupd"),
        path('adminlist/',adminlist,name="adminlist"),
        path('register/',register,name="register"),
        path('colabgc/',colabgc,name="colabgc"),
        path('colabadd/',colabadd,name="colabadd"),
        path('colabupd/',colabupd,name="colabupd"),
        path('colablist/',colablist,name="colablist"),
	]