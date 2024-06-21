from django.contrib import admin
from django.urls import path
from gestorApp import views as vista

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', vista.index,name='index'),
    path('dashboard/', vista.dashboard,name='dashboard'),
    path('clientes/', vista.clientes, name='clientes'),
    path('agendar/', vista.agendar, name='agendar'),
]
