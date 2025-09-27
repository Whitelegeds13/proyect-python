from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from app.models import Alumno,Cinturon,Docente,Horario,Matricula
from django.contrib.auth.models import User,Group
from django.db.models import Q
from datetime import datetime
from django.core.mail import send_mail

def lista_evaluar_pago_matricula(request):
    user_id = request.user.id  # Obtener el ID del usuario que ha iniciado sesión
    # Obtener el docente asociado al usuario
    docente = Docente.objects.get(id_usuario=user_id)  
    id_docente = docente.id

    # Obtener todos los horarios del docente
    horarios = Horario.objects.filter(id_docente=id_docente)  

    lista_matriculas=Matricula.objects.filter(id_horario__in=horarios)

    return render(request,'app/pagos/evaluar_pago_matricula.html',{'lista_matriculas':lista_matriculas})


def aceptar_pago_matricula(request, matricula_id):
    # Obtener la clase gratuita
    matricula = get_object_or_404(Matricula, id=matricula_id)
    
    # Cambiar el estado a aceptado
    matricula.estado = 'Pagado'
    matricula.save()
    
    # Enviar un correo electrónico de notificación
    send_mail(
        'Evaluacion del pago de matricula',
        f'Tu pago de matricula ha sido aceptada en el horario .{matricula.id_horario.frecuencia}-{matricula.id_horario.grupo}-{matricula.id_horario.id_sede.distrito}-{matricula.id_horario.hora_inicio}-{matricula.id_horario.hora_fin}',
        'from@example.com',  # Cambia esto al correo del remitente
        [matricula.id_alumno.correo],
        fail_silently=False,
    )
    
    # Agregar un mensaje de éxito
    messages.success(request, 'El pago fue aceptado correctamente')
    
    # Redirigir a la lista de solicitudes
    return redirect('lista_evaluar_pago_matricula')

def denegar_pago_matricula(request, matricula_id):
    # Obtener la clase gratuita
    matricula = get_object_or_404(Matricula, id=matricula_id)
    
    # Cambiar el estado a aceptado
    matricula.estado = 'Denegado'
    matricula.save()
    
    # Enviar un correo electrónico de notificación
    send_mail(
        'Evaluacion del pago de matricula',
        f'Tu pago de matricula ha sido aceptada en el horario .{matricula.id_horario.frecuencia}-{matricula.id_horario.grupo}-{matricula.id_horario.id_sede.distrito}-{matricula.id_horario.hora_inicio}-{matricula.id_horario.hora_fin}',
        'from@example.com',  # Cambia esto al correo del remitente
        [matricula.id_alumno.correo],
        fail_silently=False,
    )
    
    # Agregar un mensaje de éxito
    messages.success(request, 'El pago fue Denegado')
    
    # Redirigir a la lista de solicitudes
    return redirect('lista_evaluar_pago_matricula')


def lista_matricula_alumno(request):
    usuario = request.user
    alumno = Alumno.objects.get(id_usuario=usuario.id)
    
    # Filtrar las matrículas con estado "sin pagar", "denegado" o "Pagado"
    matriculas_sin_pagar_o_denegadas_o_pagadas = Matricula.objects.filter(
        Q(id_alumno=alumno) & (Q(estado="sin pagar") | Q(estado="Denegado") | Q(estado="Pagado"))
    )

    return render(request, 'app/alumnos/lista_matriculas_alumno.html', {
        'matriculas_sin_pagar_o_denegadas_o_pagadas': matriculas_sin_pagar_o_denegadas_o_pagadas
    })

def pagar_matricula_alumno(request,matricula_id):
     
    usuario = request.user
    alumno = Alumno.objects.get(id_usuario=usuario.id)
    matricula=Matricula.objects.get(id=matricula_id)
    if request.method == 'POST':
        
        if 'comprobante_pago' in request.FILES:
            matricula.comprobante_pago = request.FILES['comprobante_pago']
            try:
                matricula.save()  # Intenta guardar la sede
                messages.success(request, "Pago Enviado para ser Evaluado")  # Mensaje de éxito
            except Exception as e:
                messages.error(request, "Hubo un error en el pago: {}".format(e))  # Mensaje de error
        return redirect('lista_matricula_alumno')
            
    else:
        matricula=Matricula.objects.get(id=matricula_id)
        return render(request,'app/alumnos/pago_matricula_alumno.html',{'matricula':matricula})