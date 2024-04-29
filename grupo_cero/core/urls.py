from django.urls import path
from .views import *


urlpatterns = [
    	path('',index,name="index"),
        path('contacto/',contacto,name="contacto"),
        path('colecciones/',colecciones,name="colecciones"),
        path('artistas/',artistas,name="artistas"),
        path('coleccionessingle/',coleccionessingle,name="coleccionessingle"),
        path('obras/add/',obrasadd,name="add"),
        path('obras/update/<id>/',obrasupd,name="upd"),
	]