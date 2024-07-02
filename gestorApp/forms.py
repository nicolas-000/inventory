from django import forms
from gestorApp.models import Agenda,Cliente,Vehiculo,Atencion,Repuestos,Boleta
from gestorApp.choises import estadoReserva, tipoVehiculo,estadoAtencion
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '11111111-1'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '*************'}), label='Contraseña')

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class AgendaForm(forms.ModelForm):
    nombreAgendado = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese titulo de reserva'}))
    fechaInicio = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class' : 'form-control', 'placeholder':'Fecha y hora de inicio','type':'datetime-local','readonly':'true'}))
    fechaTermino = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class' : 'form-control', 'placeholder':'Fecha y hora de termino','type':'datetime-local','readonly':'true'}))
    telefono = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Número del cliente'}))
    tipoVehiculo = forms.ChoiceField(choices=tipoVehiculo, widget=forms.Select(attrs={'class': 'form-select'}))
    servicioSolicitado = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese tipo de servicio'}))
    descripcion = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Información Adicional'}))
    estado = forms.ChoiceField(choices=estadoReserva, widget=forms.Select(attrs={'class': 'form-select'}))
    
    class Meta:
        model = Agenda
        fields = '__all__'

class ClienteForm(forms.ModelForm):
    nombreCompleto = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre Completo'}))
    rut = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12345678-9'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'mail@mail.com'}))
    checked = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'agregarVehiculo'}), required=False)
    vehiculo_patente = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'AA-BB-00'}), required=False)
    vehiculo_marca = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Marca'}), required=False)
    vehiculo_descripcion = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripcion', 'rows': '2'}), required=False)

    class Meta:
        model = Cliente
        fields = '__all__'

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')

        if nombre and not nombre.isalpha() and ' ' not in nombre:
            raise forms.ValidationError("El nombre debe tener solo letras y espacios")
        
        return nombre

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')

        if rut and ' ' in rut:
            raise forms.ValidationError("El rut no debe contener espacios")
        
        return rut
    
class VehiculoForm(forms.ModelForm):
    marca = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Marca'}))
    patente = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'AA-BB-00'}))
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'placeholder': 'Descripción', 
            'rows': 5,  # Número de filas
            'cols': 40  # Número de columnas
        })
    )
    propietario = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        empty_label="Selecciona Cliente",
        widget=forms.Select(attrs={'class':'form-select'}),
        label="Cliente"
    )

    class Meta:
        model = Vehiculo
        fields = '__all__'

    def clean_patente(self):
        patente = self.cleaned_data.get('patente')

        if patente and ' ' in patente:
            raise forms.ValidationError("La patente no debe contener espacios")
        
        return patente
    
class AtencionForm(forms.ModelForm):
    idPropietario = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        empty_label="Selecciona Cliente",
        widget=forms.Select(attrs={'class':'form-select', 'id': 'idPropietario'}),
        label="Cliente",
    )
    fechaInicio = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Fecha de inicio', 'type': 'date'}))
    idVehiculo = forms.ModelChoiceField(
        queryset=Vehiculo.objects.all(),
        empty_label="Selecciona Vehiculo",
        widget=forms.Select(attrs={'class':'form-select', 'id': 'idVehiculo'}),
        label="Vehiculo",
    )
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'placeholder': 'Descripción', 
            'rows': 5,
            'cols': 40
        })
    )
    estado = forms.ChoiceField(choices=estadoAtencion, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Atencion
        fields = '__all__'
        
        
class RepuestoForm(forms.ModelForm):
    nombreRepuesto = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del Repuesto'}))
    marca = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Marca del Repuesto'}))
    tipoRepuesto = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tipo de repuesto'}))
    costoRepuesto = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Costo del repuesto','min': '0'}))