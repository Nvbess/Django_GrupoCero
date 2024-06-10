from django.contrib import admin
from .models import *
from django.contrib.admin import ModelAdmin
from admin_confirm import AdminConfirmMixin


# Register your models here.

class ArteAdmin(AdminConfirmMixin, ModelAdmin):
    confirm_change = True
    confirmation_fields = ['autor','descripcion','valor']

admin.site.register(Categoria)
admin.site.register(Arte, ArteAdmin)
admin.site.register(Autor)