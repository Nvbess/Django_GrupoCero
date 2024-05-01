from django.db import models

# Create your models here.

class TipoObra(models.Model):
    tipo_obra = models.CharField(max_length=50)

    def __str__(self):
        return self.tipo_obra

class Obra(models.Model):
    nombre_obra = models.CharField(max_length=200)
    autor = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=1000)
    valor = models.IntegerField(default=0)
    vendido = models.BooleanField(default=False)
    imagen = models.ImageField(upload_to='static/core/assets/img')
    tipo = models.ForeignKey(TipoObra, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.autor
