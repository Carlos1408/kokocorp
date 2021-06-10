from django.db import models


class Usuario(models.Model):
    nombre_completo = models.CharField(max_length=100)
    fecha_de_nacimiento = models.DateField()
    celular = models.BigIntegerField(unique=True)
    direccion = models.CharField(max_length=100)
    correo = models.EmailField(max_length=150, unique=True)
    contrasenia = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nombre_completo} {self.correo}"