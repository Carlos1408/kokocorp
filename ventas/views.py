from django.shortcuts import render, HttpResponse, redirect
from .models.producto import Producto
from .models.proveedor import Proveedor
from ast import literal_eval

# Create your views here.
def home(request):
    productos = Producto.objects.all()
    return render(request, 'ventas/home.html', {'productos':productos})

def producto(request, id):
    producto = Producto.objects.filter(id=id)
    producto = producto[0]
    producto.caracteristicas = literal_eval(producto.caracteristicas)
    # proveedor = Proveedor.objects.filter(id=producto.id_proveedor)
    print(producto, producto.id_proveedor)
    return render(request, 'ventas/producto.html', {'producto':producto})

def carrito(request):
    return render(request, 'ventas/carrito.html')

def categoria(request, categoria):
    print(categoria)
    productos = Producto.objects.filter(categoria=categoria)
    print(productos)
    return render(request, 'ventas/home.html', {'productos':productos})