from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    	path('',index,name="index"),
        path('contacto/',contacto,name="contacto"),
        path('colecciones/',colecciones,name="colecciones"),
        path('obra/<int:id>/',coleccion_detalle,name="coleccion_detalle"),
        path('artistas/',artistas,name="artistas"),
        path('artistasingle/',artistasingle,name="artistasingle"),
        path('admingc/',admingc,name="admingc"),
        path('adminadd/',adminadd,name="adminadd"),
        path('adminlist/',adminlist,name="adminlist"),
        path('adminlist/delete/<str:username>/',admindel,name="admindel"),
        path('adminlist/update/<str:username>/',adminupd,name="adminupd"),
        path('register/',register,name="register"),
        path('colabgc/',colabgc,name="colabgc"),
        path('colabadd/',colabadd,name="colabadd"),
        path('colabupd/',colabupd,name="colabupd"),
        path('colablist/',colablist,name="colablist"),
        path('colabautor/',colabautor,name="colabautor"),
        path('artista2/',artistas2,name="artista2"),
	]

