from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Categoria(models.Model):
    categoria = models.CharField(max_length=50)

    def __str__(self):
        return self.categoria
    
class Autor(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='images/', null=True, blank=True)

    def delete(self):
        self.imagen.delete()
        super().delete()


    def __str__(self):
        return self.nombre

class Arte(models.Model):
    titulo = models.CharField(max_length=150)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
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
    
class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

    def total(self):
        return sum(item.subtotal() for item in self.items.all())
    
class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    obra = models.ForeignKey(Arte, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.obra.titulo}"

    def subtotal(self):
        return self.obra.valor * self.cantidad
    
# NO HE PROBADO ESTO, PERO DEJE EL MODELO CREADO!
    
class Pedido(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    rut = models.CharField(max_length=10)
    telefono = models.IntegerField(default=0)
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    paypal_id = models.CharField(max_length=255, blank=True)
    paypal_status = models.CharField(max_length=50, blank=True)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    pedido_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"Pedido #{self.pedido_id} de {self.usuario.username}"
