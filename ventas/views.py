from django.shortcuts import render, HttpResponse, redirect
from .models.producto import Producto
from .models.proveedor import Proveedor
from .models.usuario import Usuario
from django.db.models import ObjectDoesNotExist
from ast import literal_eval

carrito_compra = []
cantidades = []
sesion = None
# Create your views here.
def home(request):
    productos = Producto.objects.all()
    return render(request, 'ventas/home.html', {'productos':productos, 'carrito':carrito_compra, 'sesion':sesion})

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

def categoria(request, categoria):
    print(categoria)
    productos = Producto.objects.filter(categoria=categoria)
    print(productos)
    return render(request, 'ventas/home.html', {'productos':productos})

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

def confirmar_pedido(request):
    if sesion:
        for cantidad, producto in zip(cantidades, carrito_compra):
            print(Producto.objects.get(id=producto))
        carrito_compra.clear()
        cantidades.clear()
        return redirect('home')
    else:
        return redirect('carrito')

def nueva_cuenta(request):
    return render(request, 'ventas/registro_usuario.html')

def iniciar_sesion(request):
    form_data = request.POST.dict()
    email = form_data['email']
    password = form_data['password']

    try:
        usuario = Usuario.objects.get(correo=email, contrasenia=password)
        global sesion
        sesion = usuario.correo
        print(usuario, sesion)

    except ObjectDoesNotExist:
        print('SESION NO INICIADA')

    return redirect('home')

def cerrar_sesion(request):
    global sesion
    sesion = None
    return redirect('home')

def mi_cuenta(request):
    return render(request, 'ventas/cuenta_usuario.html')