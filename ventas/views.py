from django.shortcuts import render, HttpResponse, redirect
from .models.producto import Producto
from .models.proveedor import Proveedor
from .models.usuario import Usuario
from .models.carrito import Carrito
from .models.pedido_indiv import Pedido_indiv
from django.db.models import ObjectDoesNotExist
from ast import literal_eval
from django.contrib import messages
from datetime import date

carrito_compra = []
cantidades = []
sesion = None
# Create your views here.
# CATALOGO
def home(request):
    productos = Producto.objects.all()
    # messages.add_message(request, messages.SUCCESS, 'Mensaje recibido')
    return render(request, 'ventas/home.html', {'productos':productos, 'carrito':carrito_compra, 'sesion':sesion})

def busqueda(request):
    form_data = request.POST.dict()
    busqueda = form_data['busqueda']
    print(busqueda)
    productos = Producto.objects.filter(nombre__icontains=busqueda)
    print(productos)
    return render(request, 'ventas/home.html', {'productos':productos, 'carrito':carrito_compra, 'sesion':sesion})

def producto(request, id):
    try:
        id = int(id)
        producto = Producto.objects.get(id=id)
    except:
        producto = Producto.objects.get(nombre=id)
    producto.caracteristicas = literal_eval(producto.caracteristicas)
    return render(request, 'ventas/producto.html', {'producto':producto,'carrito':carrito_compra, 'sesion':sesion})

def categoria(request, categoria):
    print(categoria)
    productos = Producto.objects.filter(categoria=categoria)
    print(productos)
    return render(request, 'ventas/home.html', {'productos':productos, 'sesion':sesion})

# CARRITO
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
    data = {'cant_productos':cant_productos, 'total':costo_total, 'sesion':sesion}
    return render(request, 'ventas/carrito.html', data)

def add_carrito(request, id):
    carrito_compra.append(int(id))
    messages.success(request, 'Producto agregado al carrito')
    print('request ->  ', request.path)
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

def confirmar_pedido(request, total):
    if sesion:
        usuario = Usuario.objects.get(correo = sesion)
        carrito = Carrito.objects.create(
            fecha = date.today(),
            id_usuario = usuario,
            costo = float(total)
        )
        for cantidad, producto in zip(cantidades, carrito_compra):
            producto = Producto.objects.get(id=producto)
            producto.stock -= cantidad
            producto.save()
            print(usuario, producto, cantidad, total)
            pedido = Pedido_indiv.objects.create(
                id_producto = producto,
                id_carrito = carrito,
                cantidad_prod = cantidad,
                costo = cantidad*producto.costo_unitario
            )
        carrito_compra.clear()
        cantidades.clear()
        messages.success(request, 'Pedido confirmado exitosamente')
        return redirect('home')
    else:
        messages.warning(request, 'Debe iniciar sesion')
        return redirect('carrito')

# USUARIO
def nueva_cuenta(request):
    if request.method == 'POST':
        form_data = request.POST.dict()
        contra = form_data['contrasenia']
        confirm = form_data['contrasenia_confirm']
        if contra == confirm:
            print('CONFIRMADO')
            try:
                usuario = Usuario.objects.create(
                    nombre_completo=form_data['nombre'],
                    fecha_de_nacimiento=form_data['fecha_nacimiento'],
                    celular=form_data['telefono'],
                    direccion=form_data['direccion'],
                    correo=form_data['correo'],
                    contrasenia=contra
                )
            except:
                messages.warning(request, 'Telefono o correo ya existentes')
                return redirect('nueva-cuenta')
            global sesion
            sesion = usuario.correo
            print(sesion)
            messages.success(request, 'Cuenta creada exitosamente')
            return redirect('mi-cuenta')
        else:
            messages.warning(request, 'Las contraseñas no coninciden')
            return redirect('nueva-cuenta')
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
        messages.success(request, 'Sesion iniciada')
    except ObjectDoesNotExist:
        messages.warning(request, 'Usuario no existente')

    return redirect('home')

def cerrar_sesion(request):
    global sesion
    sesion = None
    messages.warning(request, 'Sesion cerrada')
    return redirect('home')

def mi_cuenta(request):
    usuario = Usuario.objects.get(correo=sesion)
    return render(request, 'ventas/cuenta_usuario.html', {'sesion':sesion, 'usuario':usuario})

def historial_carrito(request):
    usuario = Usuario.objects.get(correo = sesion)
    carritos = Carrito.objects.filter(id_usuario = usuario.id)
    return render(request, 'ventas/historial_carrito.html', {'sesion':sesion, 'carritos':carritos})
    
def historial_detalle(request, carrito):
    pedidos = Pedido_indiv.objects.filter(id_carrito = carrito)
    return render(request, 'ventas/historial_detalle.html', {'sesion':sesion, 'pedidos':pedidos})