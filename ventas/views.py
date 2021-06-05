from django.shortcuts import render, HttpResponse, redirect
from .models.producto import Producto
from .models.proveedor import Proveedor
from ast import literal_eval

carrito_compra = []
cantidades = []
# Create your views here.
def home(request):
    productos = Producto.objects.all()
    return render(request, 'ventas/home.html', {'productos':productos, 'carrito':carrito_compra})

def busqueda(request):
    form_data = request.POST.dict()
    busqueda = form_data['busqueda']
    print(busqueda)
    productos = Producto.objects.filter(nombre__icontains=busqueda)
    print(productos)
    return render(request, 'ventas/home.html', {'productos':productos, 'carrito':carrito_compra})

def producto(request, id):
    producto = Producto.objects.get(id=id)
    producto.caracteristicas = literal_eval(producto.caracteristicas)
    return render(request, 'ventas/producto.html', {'producto':producto,'carrito':carrito_compra})

def carrito(request):
    costo_total = 0
    cant_productos = []
    for cant, id_p in zip(cantidades, carrito_compra):
        prod = Producto.objects.get(id=id_p)
        prod.caracteristicas = literal_eval(prod.caracteristicas)
        precio = prod.costo_unitario * cant
        costo_total += precio
        cant_productos.append((cant, prod, precio))
    print(cant_productos)
    data = {'cant_productos':cant_productos, 'total':costo_total}
    return render(request, 'ventas/carrito.html', data)

def add_carrito(request, id):
    carrito_compra.append(int(id))
    try:
        form_data = request.POST.dict()
        cantidades.append(int(form_data['cantidad']))
    except:
        cantidades.append(1)
        return redirect('home')
    print(carrito_compra)
    print(cantidades)
    return redirect(f'/producto/{id}')

def remover_carrito(request, id):
    indice = carrito_compra.index(int(id))
    carrito_compra.remove(int(id))
    cantidades.remove(cantidades[indice])
    return redirect('carrito')

def categoria(request, categoria):
    print(categoria)
    productos = Producto.objects.filter(categoria=categoria)
    print(productos)
    return render(request, 'ventas/home.html', {'productos':productos})
