from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('producto/<id>', producto, name='producto'),
    path('carrito', carrito, name='carrito'),
    path('categoria/<categoria>', categoria, name='categoria'),
    path('add-carrito/<id>', add_carrito, name='add-carrito'),
    path('remover-carrito/<id>', remover_carrito, name='remover-carrito'),
    path('busqueda', busqueda, name='busqueda'),
    path('nueva-cuenta', nueva_cuenta, name='nueva-cuenta'),
    path('mi-cuenta', mi_cuenta, name='mi-cuenta'),
    path('iniciar-sesion', iniciar_sesion, name='iniciar-sesion'),
    path('cerrar-sesion', cerrar_sesion, name='cerrar-sesion'),
    path('confirmar-pedido/<total>', confirmar_pedido, name='confirmar-pedido'),
    path('historial-carrito', historial_carrito, name='historial-carrito'),
    path('historial-detalle/<carrito>',historial_detalle, name='historial-detalle' )
]