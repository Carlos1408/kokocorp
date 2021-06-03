from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('producto/<id>', producto, name='producto'),
    path('carrito/', carrito, name='carrito'),
    path('categoria/<categoria>/', categoria, name='categoria')
]