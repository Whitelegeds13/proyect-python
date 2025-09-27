from django.shortcuts import render,redirect
from django.contrib import messages
from app.models import Docente
from app.models import Sede
from django.contrib.auth.models import User,Group
from django.db.models import Q
from datetime import datetime
from django.core.exceptions import ValidationError
import re

def editar_perfil(request, id_docente):
    docente = Docente.objects.get(id=id_docente)
    
    if request.method == "POST":
        # Captura de datos del formulario
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        correo = request.POST.get('correo')
        direccion = request.POST.get('direccion')

        # Validación de nombres y apellidos
        if nombre and not re.match("^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", nombre):
            messages.error(request, "El nombre solo puede contener letras.")
            return redirect('editar_perfil', id_docente=docente.id)
        
        if apellido and not re.match("^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", apellido):
            messages.error(request, "El apellido solo puede contener letras.")
            return redirect('editar_perfil', id_docente=docente.id)

        # Verifica si los campos están permitidos para ser actualizados
        if nombre:  # Permitir actualización de nombre
            docente.nombre = nombre
        if apellido:  # Permitir actualización de apellido
            docente.apellido = apellido
        if correo:  # Permitir actualización de correo
            docente.correo = correo
        if direccion:  # Permitir actualización de dirección
            docente.direccion = direccion

        # Guarda los cambios
        docente.save()
        messages.success(request, "Perfil actualizado exitosamente.")
        return redirect('editar_perfil', id_docente=docente.id)
    else:
        return render(request, 'app/docentes/Perfil_docente.html', {'docente': docente})