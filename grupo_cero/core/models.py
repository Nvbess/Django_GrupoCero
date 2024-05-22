from django.db import models

# Create your models here.
class Categoria(models.Model):
    categoria = models.CharField(max_length=50)

    def __str__(self):
        return self.categoria

class Arte(models.Model):
    titulo = models.CharField(max_length=150)
    autor = models.CharField(max_length=150)
    descripcion = models.TextField()
    valor = models.IntegerField(default=0)
    imagen = models.ImageField(upload_to='images/', null=True, blank=True)
    habilitado = models.BooleanField(default=False)
    mensaje = models.CharField(max_length=150, default='')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def delete(self):
        self.imagen.delete()
        super().delete()

    def __str__(self):
        return self.titulo
    
class Autor(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='images/', null=True, blank=True)

    def delete(self):
        self.imagen.delete()
        super().delete()


    def __str__(self):
        return self.nombre
