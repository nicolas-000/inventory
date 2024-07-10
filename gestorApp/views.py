from django.shortcuts import render,redirect, get_object_or_404
from gestorApp import forms
from gestorApp.forms import AgendaForm, VehiculoForm,AtencionForm,RepuestoForm,BoletaForm
from gestorApp.models import Agenda, Cliente, Vehiculo,Atencion,Repuestos,Boleta, Persona, Boleta
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Frame, PageTemplate
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.core import serializers
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import logout
from django.template.loader import get_template,render_to_string
from django.conf import settings
import os
from datetime import datetime
from xhtml2pdf import pisa


# Create your views here.
def index(req):
    return render(req, 'gestorApp/index.html')

@permission_required("gestorApp.acceso_total_app", raise_exception=True)
def custom_logout_view(request):
    logout(request)
    return redirect('login')

@permission_required("gestorApp.acceso_total_app", raise_exception=True)
def dashboard(req):
    agendas = Agenda.objects.all().order_by('fechaInicio')
    data = {
        'agendas': agendas,
    }
    return render(req, 'gestorApp/dashboard.html',data)

@permission_required("gestorApp.acceso_total_app", raise_exception=True)
def clientes(req):
    if req.method == 'POST':
        checked = req.POST.get('checked')
        form = forms.ClienteForm(req.POST)
        if form.is_valid():
            cliente_id = form.save()
            if checked == 'on':
                vehiculo = Vehiculo.objects.create(marca=form.cleaned_data.pop('vehiculo_marca'), patente=form.cleaned_data.pop('vehiculo_patente'), descripcion=form.cleaned_data.pop('vehiculo_descripcion'), propietario=cliente_id) 
            return redirect('clientes')
    else:
        form = forms.ClienteForm()

    clientes = Cliente.objects.all().annotate(num_vehiculos=Count('vehiculo'))

    return render(req, 'gestorApp/clientes.html', {'form': form, 'clientes': clientes})

@permission_required("gestorApp.acceso_total_app", raise_exception=True)
def eliminar_cliente(req, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if req.method == 'POST':
        cliente.delete()
        return JsonResponse({'message': 'Yes!'})
    return JsonResponse({'message': 'NO!'})

@permission_required("gestorApp.acceso_total_app", raise_exception=True)
def editar_cliente(req, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if req.method == 'POST':
        form = forms.ClienteForm(req.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('clientes')
        else:
            form = forms.ClienteForm(instance=cliente)
        return render(req, 'gestorApp/clientes.html', {'form': form, 'clientes': clientes})

    cliente = Persona.objects.filter(id=cliente_id)
    data = serializers.serialize('json', cliente)
    return HttpResponse(data, content_type='application/json')

#AGENDA
@permission_required("gestorApp.acceso_total_app", raise_exception=True)
def agendar(req):
    if req.method == 'POST':
        form = forms.AgendaForm(req.POST,req.FILES)
        if form.is_valid():
            form.save()
            return redirect('agendar')
    else:
        form = AgendaForm()
        
    agendas = Agenda.objects.all()
    data = {
        'form': form,
        'agendas': agendas,
    }    
        
        
    return render(req, 'gestorApp/agenda.html', data)

@csrf_exempt 
@require_POST
@permission_required("gestorApp.acceso_total_app", raise_exception=True)
def eliminarEvent(req):
    AgendadoId = req.POST.get('event_id')
    try:
        evento = Agenda.objects.get(idAgendado=AgendadoId)
        evento.delete()
        return JsonResponse({'message': 'Evento eliminado correctamente.'})
    except Agenda.DoesNotExist:
        return JsonResponse({'error': 'El evento no existe.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@permission_required("gestorApp.acceso_total_app", raise_exception=True)
def modificarEvent(req):
    AgendadoId = req.POST.get('event_id')
    start = req.POST.get('start')
    end = req.POST.get('end')
    try:
        evento = Agenda.objects.get(idAgendado=AgendadoId)
        evento.fechaInicio = start
        evento.fechaTermino = end
        evento.save()
        return JsonResponse({'message': 'Evento modificado correctamente.'})
    except Agenda.DoesNotExist:
        return JsonResponse({'error': 'El evento no existe.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    
    
    
    
    
#Atenciones
@permission_required("gestorApp.acceso_total_app", raise_exception=True)
def atenciones(request):
    if request.method == 'POST':
        form = AtencionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('atenciones')
    else:
        form = AtencionForm()

    atenciones = Atencion.objects.all()
    return render(request, 'gestorApp/atenciones.html', {'form': form, 'atenciones': atenciones})

@permission_required("gestorApp.acceso_total_app", raise_exception=True)
def get_vehiculos(request, cliente_id):
    vehiculos = Vehiculo.objects.filter(propietario_id=cliente_id)
    vehiculos_json = [{"id": vehiculo.id, "patente": vehiculo.patente, 'nombre': vehiculo.marca, 'descripcion': vehiculo.descripcion} for vehiculo in vehiculos]
    return JsonResponse({"vehiculos": vehiculos_json})


def cargar_editar_atencion(req, atencion_id):
    atencion = get_object_or_404(Atencion, id=atencion_id)
    form = AtencionForm(instance=atencion)  
      
    return render(req, 'gestorApp/modificarAtencion.html', {'form': form, 'atencion': atencion})



@permission_required("gestorApp.acceso_total_app", raise_exception=True)
def editar_atencion(req, atencion_id):
    atencion = get_object_or_404(Atencion, id=atencion_id)

    if req.method == 'POST':
        form = AtencionForm(req.POST, instance=atencion)
        if form.is_valid():
            form.save()
            return redirect('atenciones')  # Asegúrate de que 'atenciones' sea el nombre correcto de la vista a la que quieres redirigir
    else:
        form = AtencionForm(instance=atencion)
    
    return render(req, 'gestorApp/editar_atencion.html', {'form': form, 'atencion': atencion})

@permission_required("gestorApp.acceso_total_app", raise_exception=True)
def get_atenciones(request, cliente_id):
    atenciones = Atencion.objects.filter(idPropietario=cliente_id)
    atenciones_json = [{"id": atencion.id, "fechaInicio": atencion.fechaInicio, 'estado': atencion.estado, 'descripcion': atencion.descripcion} for atencion in atenciones]
    return JsonResponse({"atenciones": atenciones_json})


# Mantenedor Vehiculo -------------------------------------------------------------------
@permission_required("gestorApp.acceso_total_app", raise_exception=True)
def vehiculo_create_or_edit(request, vehiculo_id=None):
    if vehiculo_id:
        vehiculo = get_object_or_404(Vehiculo, pk=vehiculo_id)
    else:
        vehiculo = None

    if request.method == 'POST':
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            return redirect('vehiculo_create')  # Redirige a la lista de vehículos
    else:
        form = VehiculoForm(instance=vehiculo)

    vehiculos = Vehiculo.objects.all()  # Para mostrar la lista de vehículos registrados

    return render(request, 'gestorApp/vehiculo.html', {'form': form, 'vehiculos': vehiculos})

@permission_required("gestorApp.acceso_total_app", raise_exception=True)
def eliminar_vehiculo(req, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, pk=vehiculo_id)
    vehiculo.delete()
    return redirect('vehiculo_create')


@permission_required("gestorApp.acceso_total_app", raise_exception=True)
def agregar_repuesto(request, atencion_id):
    atencion = get_object_or_404(Atencion, pk=atencion_id)
    repuestos = Repuestos.objects.filter(atencion=atencion)

    if request.method == "POST":
        form = RepuestoForm(request.POST)
        if form.is_valid():
            nuevo_repuesto = form.save(commit=False)
            nuevo_repuesto.atencion = atencion
            nuevo_repuesto.save()
            return redirect('agregar_repuesto', atencion_id=atencion.id)
    else:
        form = RepuestoForm()

    return render(request, 'gestorApp/agregar_repuesto.html', {
        'atencion': atencion,
        'form': form,
        'repuestos': repuestos
    })
#boleta 2.0
def generar_boleta(request, atencion_id):
    atencion = get_object_or_404(Atencion, id=atencion_id)
    repuestos = Repuestos.objects.filter(atencion=atencion)
    
    subtotal = sum(repuesto.costoRepuesto * repuesto.cantidad for repuesto in repuestos)
    
    if request.method == 'POST':
        form = BoletaForm(request.POST)
        if form.is_valid():
            boleta = form.save(commit=False)
            boleta.atencion = atencion
            boleta.subtotal = subtotal
            boleta.total = boleta.totalMO + subtotal
            boleta.save()
            return redirect('detalle_boleta', boleta.id)
    else:
        form = BoletaForm()

    context = {
        'atencion': atencion,
        'repuestos': repuestos,
        'subtotal': subtotal,
        'form': form
    }
    return render(request, 'gestorApp/generar_boleta.html', context)

def detalle_boleta(request, atencion_id):
    atencion = get_object_or_404(Atencion, pk=atencion_id)
    boleta = get_object_or_404(Boleta, atencion=atencion)
    repuestos = Repuestos.objects.filter(atencion=atencion)
    
    return render(request, 'gestorApp/detalle_boleta.html', {
        'atencion': atencion,
        'boleta': boleta,
        'repuestos': repuestos
    })
    
    
def generar_pdf_boleta(request, atencion_id):
    atencion = get_object_or_404(Atencion, id=atencion_id)
    boleta = get_object_or_404(Boleta, atencion=atencion)
    repuestos = Repuestos.objects.filter(atencion=atencion)
    
    # Calcular el costo total de repuestos y el total de todo
    subtotal = sum(repuesto.costoRepuesto * repuesto.cantidad for repuesto in repuestos)
    total = subtotal + boleta.totalMO
    
    # Renderizar la plantilla HTML con el contexto
    html = render_to_string('gestorApp/boletaTotal.html', {
        'atencion': atencion,
        'boleta': boleta,
        'repuestos': repuestos,
        'subtotal': subtotal,
        'total': total
    })
    
    # Crear el objeto HttpResponse con el tipo de contenido adecuado
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="boleta_{atencion.id}.pdf"'
    
    # Crear el PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    # Verificar si hay errores
    if pisa_status.err:
        return HttpResponse('Hubo un error al generar el PDF', status=400)
    
    return response
    