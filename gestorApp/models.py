from django.db import models
from gestorApp.choises import estadoReserva,tipoVehiculo,estadoAtencion

class Persona(models.Model):
    nombreCompleto = models.CharField(max_length=150)
    rut = models.CharField(max_length=13)
    email = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.nombreCompleto

class Cliente(Persona):
    def __str__(self):
        return self.nombreCompleto

class Administrativa(Persona):
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Agenda(models.Model):
    idAgendado = models.AutoField(primary_key=True)
    nombreAgendado = models.CharField(max_length=100)
    fechaInicio = models.DateTimeField()
    fechaTermino = models.DateTimeField()
    telefono = models.CharField(max_length=15)
    tipoVehiculo = models.CharField(max_length=2, choices=tipoVehiculo, default='VP')
    servicioSolicitado = models.CharField(max_length=100, blank=True, null=True) 
    descripcion = models.TextField(blank=True, null=True)  
    estado = models.CharField(max_length=1, choices=estadoReserva, default='P')  
    fechaCreacion = models.DateTimeField(auto_now_add=True)  
    fechaActualizacion = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return self.name

class Vehiculo(models.Model):
    marca = models.CharField(max_length=100)
    patente = models.CharField(max_length=10)
    descripcion = models.TextField()
    propietario = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.marca

class Atencion(models.Model):
    idPropietario = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    idVehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    fechaInicio = models.DateField()
    descripcion = models.CharField(max_length=300)
    estado = models.CharField(max_length=2, choices=estadoAtencion, blank=True, null=True)

    def __str__(self):
        return f"Atención {self.id} - {self.idPropietario.nombre}"

class Repuestos(models.Model):
    nombreRepuesto= models.CharField(max_length=200)
    atencion = models.ForeignKey(Atencion,on_delete=models.CASCADE)
    marca= models.CharField(max_length=100)
    costoRepuesto= models.PositiveIntegerField()

    def __str__(self):
        return self.name
    

class Boleta(models.Model):
    atencion = models.ForeignKey(Atencion, on_delete=models.CASCADE)
    repuesto = models.ForeignKey(Repuestos,on_delete=models.CASCADE)
    totalMO = models.PositiveIntegerField()
    fechaPago = models.DateField()
    

    def __str__(self):
        return f"Boleta {self.id} - Atención {self.atencion.id}"