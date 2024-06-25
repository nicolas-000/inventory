from django.shortcuts import render,redirect, get_object_or_404
from gestorApp import forms
from gestorApp.models import Agenda, Cliente

# Create your views here.
def index(req):
    return render(req, 'gestorApp/index.html')

def dashboard(req):
    return render(req, 'gestorApp/dashboard.html')

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
