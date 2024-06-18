from django.shortcuts import render

# Create your views here.
def index(req):
    return render(req, 'gestorApp/index.html')

def dashboard(req):
    return render(req, 'gestorApp/dashboard.html')

def clientes(req):
    return render(req, 'gestorApp/clientes.html')

def agenda(req):
    return render(req, 'gestorApp/agenda.html')
