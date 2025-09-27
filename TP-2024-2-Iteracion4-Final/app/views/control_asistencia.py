from django.shortcuts import render,redirect,get_object_or_404
from app.models import Docente, Horario, Sede,Alumno,Matricula,Asistencia,Asistencia_alumno
from datetime import datetime
from django.contrib import messages

def control_asistencia(request):
    usuario = request.user
    docente = Docente.objects.get(id_usuario=usuario)

    # Obtener todas las sedes asociadas a los horarios del docente
    sedes = Sede.objects.filter(horario__id_docente=docente).distinct()

    # Convertir las sedes a un formato adecuado (ID como string)
    sedes = [{"id": str(sede.id), "nombre": f"{sede.departamento} - {sede.distrito} - {sede.direccion}"} for sede in sedes]

    # Obtener el filtro de sede desde el formulario
    sede_id = request.GET.get('sede')

    # Filtrar los horarios por docente y sede seleccionada (si existe)
    if sede_id:
        horarios = Horario.objects.filter(id_docente=docente, id_sede_id=sede_id)
    else:
        horarios = Horario.objects.filter(id_docente=docente)

    # Pasar los datos al contexto
    contexto = {
        'horarios': horarios,
        'sedes': sedes,  # Lista de sedes
    }
    return render(request, 'app/Asistencia/control_asistencia_docente.html', contexto)

def lista_control_asistencia(request, id_horario):
    fecha_hora_actual = datetime.now()
    horario = Horario.objects.get(id=id_horario)
    matriculas = Matricula.objects.filter(id_horario=horario)

    if request.method == 'POST':
        try:
            # Registrar la nueva asistencia
            asistencia = Asistencia(id_horario=horario, fecha=fecha_hora_actual)
            asistencia.save()

            # Guardar el estado de asistencia para cada alumno
            for matricula in matriculas:
                alumno_id = matricula.id_alumno.id
                estado = request.POST.get(f'estado_{alumno_id}')  # Obtener el estado del alumno

                if estado:  # Verificar que el estado no esté vacío
                    asistencia_alumno = Asistencia_alumno(id_asistencia=asistencia, id_alumno=matricula.id_alumno, estado=estado)
                    asistencia_alumno.save()

            # Mensaje de éxito después de guardar la nueva asistencia
            messages.success(request, "La asistencia se ha registrado correctamente.")
        except Exception as e:
            # Mensaje de error si ocurre algún problema al registrar
            messages.error(request, f"Hubo un error al registrar la asistencia: {e}")

        return redirect('lista_control_asistencia', id_horario=id_horario)

    else:
        asistencia = Asistencia.objects.filter(id_horario=horario)
        contexto = {
            'horario': horario,
            'alumnos': matriculas,
            'asistencia': asistencia
        }
        return render(request, 'app/Asistencia/lista_control_asistencia.html', contexto)

def editar_control_asistencia(request, id_asistencia):
    # Obtener la asistencia o devolver un error 404 si no existe
    asistencia = get_object_or_404(Asistencia, id=id_asistencia)
    asistencias_alumno = asistencia.asistencia_alumno_set.all()

    if request.method == 'POST':
        try:
            # Procesar los datos enviados por el formulario
            for alumno_asistencia in asistencias_alumno:
                # Obtener el estado del alumno del formulario
                estado = request.POST.get(f'estado_{alumno_asistencia.id_alumno.id}')
                if estado in ['presente', 'ausente', 'tarde']:
                    alumno_asistencia.estado = estado
                    alumno_asistencia.save()

            # Obtener el id_horario asociado a esta asistencia
            id_horario = asistencia.id_horario.id  # Relación definida en el modelo

            # Mensaje de éxito después de guardar los cambios
            messages.success(request, "La asistencia se ha actualizado con éxito.")
        except Exception as e:
            # Mensaje de error en caso de que ocurra un problema
            messages.error(request, f"Hubo un error al actualizar la asistencia: {e}")

        return redirect('lista_control_asistencia', id_horario=id_horario)  # Redirigir con el parámetro

    # Renderizar la plantilla con el contexto
    contexto = {'asistencias_alumno': asistencias_alumno, 'asistencia': asistencia}
    return render(request, 'app/Asistencia/editar_asistencia_alumno.html', contexto)


def miAsistenciaAlumno(request):
    usuario = request.user
    alumno = Alumno.objects.get(id_usuario=usuario)
    asistencias = Asistencia_alumno.objects.filter(id_alumno=alumno).order_by('-id_asistencia__fecha')  # Orden descendente
    contexto = {'asistencias': asistencias}
    return render(request, 'app/Asistencia_alumno/asistencia_alumno.html', contexto)

    

