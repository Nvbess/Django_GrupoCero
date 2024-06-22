from django.contrib import admin
from .models import *
from django.contrib.admin import ModelAdmin
from admin_confirm import AdminConfirmMixin


# Register your models here.

class ArteAdmin(AdminConfirmMixin, ModelAdmin):
    confirm_change = True
    confirmation_fields = ['autor','descripcion','valor']

class AutorAdmin(AdminConfirmMixin, ModelAdmin):
    confirm_change = True
    confirmation_fields = ['nombre','descripcion','imagen']

admin.site.register(Categoria)
admin.site.register(Arte, ArteAdmin)
admin.site.register(Autor, AutorAdmin)
admin.site.register(Carrito)
admin.site.register(ItemCarrito)
admin.site.register(VoucherCompra)