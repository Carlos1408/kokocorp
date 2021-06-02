from django.db import models
from .proveedor import Proveedor 

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    categoria = models.CharField(default='Ninguna', max_length=50)
    costo_unitario = models.FloatField()
    stock = models.IntegerField()
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    descripcion = models.TextField(max_length= 2000)
    imagen = models.TextField(max_length=1000)
    caracteristicas = models.CharField(max_length= 500)


    def __str__(self):
	    return self.nombre