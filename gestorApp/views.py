from django.shortcuts import render,redirect, get_object_or_404
from gestorApp import forms
from gestorApp.forms import AgendaForm, VehiculoForm,AtencionForm,RepuestoForm
from gestorApp.models import Agenda, Cliente, Vehiculo,Atencion,Repuestos,Boleta, Persona
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.core import serializers
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import logout
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.conf import settings
import os
from datetime import datetime


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



#BOLETA
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = HttpResponse(content_type='application/pdf')
    pisa_status = pisa.CreatePDF(html, dest=result)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return result

def generate_pdf_view(request, atencion_id):
    data = get_object_or_404(Atencion, id=atencion_id)
    context = {'data': str(data)}
    template = 'gestorApp/boleta.html'
    pdf = render_to_pdf(template, context)

    # Save the PDF
    pdf_filename = 'boleta-' + str(datetime.now()) + ".pdf"
    pdf_path = os.path.join(settings.BOLETA_PDF_DIR, pdf_filename)
    with open(pdf_path, 'wb') as f:
        pisa_status = pisa.CreatePDF(pdf.content, dest=f)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + pdf.content + '</pre>')

    return HttpResponse(f'PDF generated and saved as {pdf_filename}')

def serve_pdf_view(request, filename):
    pdf_path = os.path.join(settings.BOLETA_PDF_DIR, filename)
    if os.path.exists(pdf_path):
        return FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')
    else:
        raise Http404