from django.shortcuts import render,redirect
from django.contrib import messages
from app.models import Docente,Alumno
from app.models import Sede
from django.contrib.auth.models import User,Group
from django.db.models import Q
from datetime import datetime
from django.core.exceptions import ValidationError
import re

def editar_perfil_alumno(request, id_alumno):
    alumno = Alumno.objects.get(id=id_alumno)
    
    if request.method == "POST":
        # Captura de datos del formulario
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        correo = request.POST.get('correo')
        direccion = request.POST.get('direccion')

        # Validación de nombres y apellidos
        if nombre and not re.match("^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", nombre):
            messages.error(request, "El nombre solo puede contener letras.")
            return redirect('editar_perfil_alumno', id_alumno=alumno.id)
        
        if apellido and not re.match("^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", apellido):
            messages.error(request, "El apellido solo puede contener letras.")
            return redirect('editar_perfil_alumno', id_alumno=alumno.id)

        # Verifica si los campos están permitidos para ser actualizados
        if nombre:  # Permitir actualización de nombre
            alumno.nombre = nombre
        if apellido:  # Permitir actualización de apellido
            alumno.apellido = apellido
        if correo:  # Permitir actualización de correo
            alumno.correo = correo
        if direccion:  # Permitir actualización de dirección
            alumno.direccion = direccion

        # Guarda los cambios
        alumno.save()
        messages.success(request, "Perfil actualizado exitosamente.")
        return redirect('editar_perfil_alumno', id_alumno=alumno.id)
    else:
        return render(request, 'app/alumnos/Perfil_alumno.html', {'alumno': alumno})