from django.contrib import admin
from django.urls import path
from gestorApp import views as vista

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', vista.index,name='index'),
    path('dashboard/', vista.dashboard,name='dashboard'),
    path('clientes/', vista.clientes, name='clientes'),
    path('eliminar_cliente/<int:cliente_id>', vista.eliminar_cliente, name='eliminar_cliente'),
    
    # Agenda
    path('agendar/', vista.agendar, name='agendar'),
    path('eliminarEvent/', vista.eliminarEvent, name='eliminarEvent'),
    path('modificarEvent/', vista.modificarEvent, name='modificarEvent'),
]
