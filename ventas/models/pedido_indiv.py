from django.db import models
from .producto import Producto
from .carrito import Carrito

class Pedido_indiv(models.Model):
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    id_carrito = models.ForeignKey(Carrito,on_delete=models.CASCADE)
    cantidad_prod = models.IntegerField()
    costo = models.FloatField()

    def __str__(self):
	    return f"{self.id_producto} {self.cantidad_prod} // {self.id_carrito}" 