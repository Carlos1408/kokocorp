from django.contrib import admin
from .models.carrito import Carrito
from .models.pedido_indiv import Pedido_indiv
from .models.producto import Producto
from .models.proveedor import Proveedor
from .models.usuario import Usuario
# Register your models here.


admin.site.register(Carrito)
admin.site.register(Pedido_indiv)
admin.site.register(Producto)
admin.site.register(Proveedor)
admin.site.register(Usuario)
