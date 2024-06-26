from django.shortcuts import render,redirect, get_object_or_404
from gestorApp import forms
from gestorApp.forms import AgendaForm, VehiculoForm,AtencionForm
from gestorApp.models import Agenda, Cliente, Vehiculo,Atencion,Repuestos,Boleta, Persona
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.core import serializers


# Create your views here.
def index(req):
    return render(req, 'gestorApp/index.html')

def dashboard(req):
    agendas = Agenda.objects.all().order_by('fechaInicio')
    data = {
        'agendas': agendas,
    }
    return render(req, 'gestorApp/dashboard.html',data)

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

def eliminar_cliente(req, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if req.method == 'POST':
        cliente.delete()
        return JsonResponse({'message': 'Yes!'})
    return JsonResponse({'message': 'NO!'})

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


def get_vehiculos(request, cliente_id):
    vehiculos = Vehiculo.objects.filter(propietario_id=cliente_id)
    vehiculos_json = [{"id": vehiculo.id, "patente": vehiculo.patente, 'nombre': vehiculo.marca, 'descripcion': vehiculo.descripcion} for vehiculo in vehiculos]
    return JsonResponse({"vehiculos": vehiculos_json})

def eliminar_atencion(req, atencion_id):
    atencion = get_object_or_404(Atencion, id=atencion_id)

    if req.method == 'POST':
        atencion.delete()
        return JsonResponse({'message': 'Yes!'})
    return JsonResponse({'message': 'NO!'})

def editar_atencion(req, atencion_id):
    atencion = get_object_or_404(Atencion, id=atencion_id)

    if req.method == 'POST':
        form = AtencionForm(req.POST, instance=atencion)
        if form.is_valid():
            form.save()
            return redirect('atenciones')
    else:
        form = AtencionForm(instance=atencion)
    return render(req, 'gestorApp/atenciones.html', {'form': form, 'atenciones': atenciones})




# Mantenedor Vehiculo -------------------------------------------------------------------
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



#BOLETA

