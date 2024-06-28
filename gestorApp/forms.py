from django import forms
from gestorApp.models import Agenda, Cliente,Vehiculo
from gestorApp.choises import estadoReserva, tipoVehiculo  

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