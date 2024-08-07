# Gestor del Taller Mecánico
## Descripción
Este proyecto surge como respuesta a la necesidad de optimizar los procesos operativos y administrativos dentro del taller mecánico, con el fin de mejorar la eficiencia, la productividad y la experiencia tanto para los clientes como para el personal.
## Instalación
### Requisitos
Python >= 3.11
### Instalar dependencias
```bash
$ pip install -r requirements.txt
```
### Realizar las migraciones a la base de datos
```bash
$ python manage.py makemigrations
```
```bash
$ python manage.py migrate
```
### Realizar cambio del estado del debug
##### tallerMecanico/settings.py
```python
DEBUG = False      # Asegurarse de cambiar el atributo a False
```
### Cambiar la clave secreta
```bash
$ python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
``` 
El resultado del comando es tu clave secreta
##### tallerMecanico/settings.py
```python
SECRET_KEY = 'tu-clave-secreta'    # Asegurarse de cambiar la clave secreta
```
### Crear superusuario para acceder a la aplicación
```bash
$ python manage.py createsuperuser
```
### Ejecutar la aplicación
```bash
$ python manage.py runserver
```
Por defecto la aplicación se ejecuta en `http://localhost:8000/`, abre un navegador e ingresa la dirección para ver la aplicación.