from django.db import models


class Usuario(models.Model):
    nombre_completo = models.CharField(max_length=100)
    fecha_de_nacimiento = models.DateField()
    celular = models.BigIntegerField()
    direccion = models.CharField(max_length=100)
    correo = models.EmailField(max_length=150)
    contrasenia = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre_completo

    # @staticmethod
	# def emailExiste(userEmail):
	# 	try:
	# 		correo = Usuario.objects.get(correo=userEmail)
	# 		return correo
	# 	except:
	# 		return False