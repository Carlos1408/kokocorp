from django.db import models
from .usuario import Usuario
import datetime


class Carrito(models.Model):
    fecha = models.DateTimeField(default=datetime.datetime.today)
    id_usuario = models.ForeignKey(Usuario, on_delete = models.CASCADE)
    costo = models.IntegerField()


    def __str__(self):
	    return self.id_usuario