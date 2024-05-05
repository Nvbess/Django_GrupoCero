from django.db import models

# Create your models here.
class Colaborador(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre

class Autor(models.Model):
    nombre_autor = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=500)

    def __str__(self):
        return self.nombre_autor

class Tipo_Arte(models.Model):
    tipoarte = models.CharField(max_length=50)

    def __str__(self):
        return self.tipoarte

class Arte(models.Model):
    nombre_arte = models.CharField(max_length=150)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=1000)
    valor = models.IntegerField(default=0)
    imagen = models.ImageField(upload_to='static/core/assets/img/', default='')
    habilitado = models.BooleanField(default=False)
    tipoarte = models.ForeignKey(Tipo_Arte, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_arte
