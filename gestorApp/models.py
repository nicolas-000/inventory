from django.db import models

class Persona(models.Model):
    nombreCompleto = models.CharField(max_length=150)
    rut = models.CharField(max_length=13)

    def __str__(self):
        return self.name

class Cliente(Persona):
    def __str__(self):
        return self.name

class Administrativa(Persona):
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Agenda(models.Model):
    nombreAgendado: models.CharField(max_length=100)
    fechaHora: models.DateTimeField()
    telefono: models.CharField(max_length=15)
    tipoVehiculo: models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Vehiculo(models.Model):
    marca: models.CharField(max_length=100)
    patente: models.CharField(max_length=8)
    descripcion: models.CharField(max_length=300)
    
    def __str__(self):
        return self.name

class Atencion(models.Model):
    descripcion: models.CharField(max_length=300)
    fechaInicio: models.DateField()
    fechaTermino: models.DateField()
    costos: models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Respuestos(models.Model):
    nombreRepuesto: models.CharField(max_length=200)
    marca: models.CharField(max_length=100)
    tipoRepuesto: models.IntegerField()
    costoRepuesto: models.PositiveIntegerField()

    def __str__(self):
        return self.name
    
class Boleta(models.Model):
    fechaPago: models.DateField()

    def __str__(self):
        return self.name