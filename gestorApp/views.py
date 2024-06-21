from django.shortcuts import render,redirect
from gestorApp.forms import AgendaForm
from gestorApp.models import Agenda

# Create your views here.
def index(req):
    return render(req, 'gestorApp/index.html')

def dashboard(req):
    return render(req, 'gestorApp/dashboard.html')

def clientes(req):
    return render(req, 'gestorApp/clientes.html')

def agendar(req):
    if req.method == 'POST':
        form = AgendaForm(req.POST,req.FILES)
        if form.is_valid():
            form.save()
            return redirect('agendar')
    else:
        form = AgendaForm()
    return render(req, 'gestorApp/agenda.html', {'form': form})
