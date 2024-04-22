from django.db import models

# Create your models here.

class TipoObra(models.Model):
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion

class Obra(models.Model):
    nombre_obra = models.CharField(max_length=200)
    autor = models.CharField(max_length=20)
    fecha = models.DateField()
    descripcion = models.CharField(max_length=500)
    valor = models.IntegerField(default=0)
    vendido = models.BooleanField(default=True)
    tipo = models.ForeignKey(TipoObra, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.autor
