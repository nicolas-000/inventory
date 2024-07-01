from django.contrib import admin
from django.urls import path
from gestorApp import views as vista

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', vista.index,name='index'),
    path('dashboard/', vista.dashboard,name='dashboard'),
    path('clientes/', vista.clientes, name='clientes'),
    path('eliminar_cliente/<int:cliente_id>/', vista.eliminar_cliente, name='eliminar_cliente'),
    path('editar_cliente/<int:cliente_id>/', vista.editar_cliente, name='editar_cliente'),
    
    # Agenda
    path('agendar/', vista.agendar, name='agendar'),
    path('eliminarEvent/', vista.eliminarEvent, name='eliminarEvent'),
    path('modificarEvent/', vista.modificarEvent, name='modificarEvent'),
    
    #atenciones
    path('atenciones/', vista.atenciones, name='atenciones'),
    path('get_vehiculos/<int:cliente_id>/', vista.get_vehiculos, name='get_vehiculos'),
    path('eliminar_atencion/<int:atencion_id>/', vista.eliminar_atencion, name='eliminar_atencion'),
    path('editar_atencion/<int:atencion_id>/', vista.editar_atencion, name='editar_atencion'),
    
    
    # Vehiculo
    path('vehiculo/', vista.vehiculo_create_or_edit, name='vehiculo_create'),
    path('vehiculo/editar/<int:vehiculo_id>/', vista.vehiculo_create_or_edit, name='editar_vehiculo'),
]
