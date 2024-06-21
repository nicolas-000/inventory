from django import forms
from gestorApp.models import Agenda
from gestorApp.choises import estadoReserva, tipoVehiculo  

class AgendaForm(forms.ModelForm):
    nombreAgendado = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese titulo de reserva'}))
    fechaHora = forms.DateTimeField(widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el día de reserva', 'type': 'date'}))
    telefono = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Número del cliente'}))
    tipoVehiculo = forms.ChoiceField(choices=tipoVehiculo, widget=forms.Select(attrs={'class': 'form-select'}))
    servicioSolicitado = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese tipo de servicio'}))
    descripcion = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Información Adicional'}))
    estado = forms.ChoiceField(choices=estadoReserva, widget=forms.Select(attrs={'class': 'form-select'}))
    
    class Meta:
        model = Agenda
        fields = '__all__'