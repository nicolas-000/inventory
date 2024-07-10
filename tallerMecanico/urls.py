from django.contrib import admin
from django.urls import path, include
from gestorApp import views as vista
from django.contrib.auth import views as auth_views
from gestorApp.forms import CustomAuthenticationForm


urlpatterns = [
    path('', auth_views.LoginView.as_view(authentication_form=CustomAuthenticationForm), name='login'),
    path('logout/', vista.custom_logout_view, name='logout'),
    path('admin/', admin.site.urls),
    # path('', vista.index,name='index'),
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
    path('atencionEdit/<int:atencion_id>/', vista.cargar_editar_atencion, name='modificarAtencion'),
    path('editar_atencion/<int:atencion_id>/', vista.editar_atencion, name='editar_atencion'),
    path('get_atenciones/<int:cliente_id>/', vista.get_atenciones, name='get_atenciones'),
    
    #repuestos
    path('atencion/<int:atencion_id>/repuestos/agregar/', vista.agregar_repuesto, name='agregar_repuesto'),

    
    # Vehiculo
    path('vehiculo/', vista.vehiculo_create_or_edit, name='vehiculo_create'),
    path('vehiculo/editar/<int:vehiculo_id>/', vista.vehiculo_create_or_edit, name='editar_vehiculo'),
    path('eliminar_vehiculo/<int:vehiculo_id>/', vista.eliminar_vehiculo, name='eliminar_vehiculo'),

    
    
    #Boleta
    path('atenciones/<int:atencion_id>/boleta/generar/', vista.generar_boleta, name='generar_boleta'),
    path('atenciones/<int:atencion_id>/boleta/detalle/', vista.detalle_boleta, name='detalle_boleta'),
    path('atenciones/<int:atencion_id>/boleta/pdf/', vista.generar_pdf_boleta, name='generar_pdf_boleta'),
    
    
]

