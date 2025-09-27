from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from app.models import Docente,Alumno,Matricula,Clase_Gratis,Horario,Asistencia,Asistencia_alumno
import matplotlib.pyplot as plt
from io import BytesIO
import base64  
import json
from django.db.models import Sum,Count, Sum
from datetime import datetime


def dashboard_admin(request):
    # Obtener los datos reales
    docentes = Docente.objects.all()
    total_alumnos= len(Alumno.objects.all())
    matriculas_pagadas = Matricula.objects.aggregate(total=Sum('monto'))['total'] or 0
    total_solicitudes=len(Matricula.objects.all())
    total_docentes = len(docentes)
    nombres_docentes = [f"{docente.nombre} {docente.apellido}" for docente in docentes]
    alumnos_por_docente = [
        Matricula.objects.filter(id_horario__id_docente=docente).count()
        for docente in docentes
    ]

    # Pasar los datos como JSON al contexto
    context = {
        'labels': json.dumps(nombres_docentes),  # Convertimos la lista en JSON
        'data': json.dumps(alumnos_por_docente), 
        'total_alumnos':total_alumnos, # Convertimos la lista en JSON
        'matriculas_pagadas':matriculas_pagadas,
        'total_solicitudes':total_solicitudes,
        'total_docentes':total_docentes
    }

    return render(request, 'app/dashboard/dashboard_admin.html', context)

def dashborad_docente(request):
    usuario = request.user
    docente = Docente.objects.get(id_usuario=usuario)

    # Filtrar horarios del docente
    horarios = Horario.objects.filter(id_docente=docente)

    # Filtrar matrículas asociadas a esos horarios
    matriculas = Matricula.objects.filter(id_horario__in=horarios)

    # Filtrar matrículas pagadas
    matriculas_pagadas = matriculas.filter(estado='Pagado')
    total_m_pagas = matriculas_pagadas.count()

    # Sumar el monto de las matrículas pagadas
    total_monto_pagado = matriculas_pagadas.aggregate(total=Sum('monto'))['total'] or 0

    # Contar alumnos totales en las matrículas
    alumnos = Alumno.objects.filter(id__in=matriculas.values_list('id_alumno', flat=True)).count()

    # Contar solicitudes de clases gratuitas para los horarios del docente
    lista_solicitudes = Clase_Gratis.objects.filter(id_horario__in=horarios).count()

    # Alumnos por horario (basado en asistencia real)
    asistencia_por_horario = (
        Asistencia_alumno.objects
        .filter(id_asistencia__id_horario__in=horarios)  # Solo los horarios del docente
        .values('id_asistencia__id_horario__grupo')  # Agrupar por grupo de horario
        .annotate(num_asistentes=Count('id_alumno'))  # Contar alumnos presentes
        .order_by('-num_asistentes')  # Ordenar de mayor a menor
    )

    # Preparar datos para el gráfico
    labels = [entry['id_asistencia__id_horario__grupo'] for entry in asistencia_por_horario]
    data = [entry['num_asistentes'] for entry in asistencia_por_horario]

    # Asegurarse de que las listas están correctamente formateadas
    labels = labels if labels else ['Sin datos']
    data = data if data else [0]

    contexto = {
        'docente': docente,
        'alumnos': alumnos,
        'total_monto_pagado': total_monto_pagado,
        'lista_solicitudes': lista_solicitudes,
        'total_m_pagas': total_m_pagas,
        'labels': labels,  # Para el gráfico
        'data': data,      # Para el gráfico
    }

    return render(request, 'app/dashboard/dashboard_docente.html', contexto)

def dashboard_alumno(request):
    usuario = request.user
    alumno = Alumno.objects.get(id_usuario=usuario.id)
    
    # Establecer estadísticas
    matricula = Matricula.objects.filter(id_alumno=alumno).first()
    asistencias_del_mes = Asistencia_alumno.objects.filter(id_alumno=alumno, id_asistencia__fecha__month=datetime.now().month).count()
    clases_completadas = Asistencia_alumno.objects.filter(id_alumno=alumno).count()
    
    # Progreso de cinturón
    grado_cinturon = alumno.grado_cinturon.color_cinturon if alumno.grado_cinturon else "Sin grado"

    # Datos para el gráfico de barras
    asistencias_por_horario = Asistencia_alumno.objects.filter(id_alumno=alumno).values('id_asistencia__id_horario').annotate(total_asistencias=Count('id_asistencia')).order_by('total_asistencias')

    # Preparar datos para el gráfico
    labels = [f"Horario {asistencia['id_asistencia__id_horario']}" for asistencia in asistencias_por_horario]
    data = [asistencia['total_asistencias'] for asistencia in asistencias_por_horario]
    
    contexto = {
        'alumno': alumno,
        'matricula': matricula,
        'asistencias_del_mes': asistencias_del_mes,
        'clases_completadas': clases_completadas,
        'grado_cinturon': grado_cinturon,
        'labels': labels,
        'data': data,
    }
    
    return render(request, 'app/dashboard/dashboard_alumno.html', contexto)
