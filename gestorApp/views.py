from django.shortcuts import render,redirect, get_object_or_404
from gestorApp import forms
from gestorApp.forms import AgendaForm, VehiculoForm
from gestorApp.models import Agenda, Cliente, Vehiculo
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

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
        form = forms.ClienteForm(req.POST)
        print(req.POST.get('checked'))
        if form.is_valid():
            form.save()
            return redirect('clientes')
    else:
        form = forms.ClienteForm()

    return render(req, 'gestorApp/clientes.html', {'form': form, 'clientes': Cliente.objects.all()})

def eliminar_cliente(req, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if req.method == 'POST':
        cliente.delete()
        return redirect('clientes')
        
    return redirect('clientes')


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
def atenciones(req):
    
    return render(req, 'gestorApp/atenciones.html')


# Mantenedor Vehiculo -------------------------------------------------------------------
def vehiculo_create(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirige a una vista que lista los vehículos, por ejemplo
    else:
        form = VehiculoForm()
    vehiculos = Vehiculo.objects.all()
    return render(request, 'gestorApp/vehiculo.html', {'form': form, 'vehiculos': vehiculos})
