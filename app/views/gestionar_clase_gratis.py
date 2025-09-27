from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User,Group
from django.db.models import Q
from datetime import datetime
from app.models import Docente,Clase_Gratis,Horario
from django.core.mail import send_mail

def lista_Clase_gratis(request):
    user_id = request.user.id  # Obtener el ID del usuario que ha iniciado sesión
    # Obtener el docente asociado al usuario
    docente = Docente.objects.get(id_usuario=user_id)  
    id_docente = docente.id

    # Obtener todos los horarios del docente
    horarios = Horario.objects.filter(id_docente=id_docente)  

    # Obtener las solicitudes de clases gratis asociadas a los horarios del docente
    lista_solicitudes = Clase_Gratis.objects.filter(id_horario__in=horarios)  # Usar __in para filtrar por múltiples IDs de horarios

    # Renderizar la plantilla con la lista de solicitudes
    return render(request, 'app/clase_gratis/lista_clase_gratis.html', {"lista_solicitudes": lista_solicitudes})

def aceptar_clase_gratis(request, clase_id):
    # Obtener la clase gratuita
    clase = get_object_or_404(Clase_Gratis, id=clase_id)
    
    # Cambiar el estado a aceptado
    clase.estado = 'aceptado'
    clase.save()
    
    # Mensaje adicional con los elementos a traer
    mensaje_adicional = """
    A continuación, te recordamos lo que debes traer al entrenamiento:
    - Buzo deportivo o short deportivo , polo blanco o negro.
    - Uñas recortadas
    - No se permiten aretes ni accesorios
    - Traer agua fría (no agua helada)
    
    Al momento de ingresar a la sede, por favor pregunta por el docente de la sede.
    """
    
    # Enviar un correo electrónico de notificación
    send_mail(
        'Solicitud de clase gratuita aceptada',
        f'Tu solicitud de clase gratuita ha sido aceptada en el horario.\n{clase.id_horario.frecuencia}-{clase.id_horario.grupo}-{clase.id_horario.id_sede.distrito}-{clase.id_horario.hora_inicio}-{clase.id_horario.hora_fin}\n\n{mensaje_adicional}',
        'from@example.com',  # Cambia esto al correo del remitente
        [clase.correo],
        fail_silently=False,
    )
    
    # Agregar un mensaje de éxito
    messages.success(request, 'La solicitud ha sido aceptada y se ha enviado un correo electrónico al solicitante.')
    
    # Redirigir a la lista de solicitudes
    return redirect('lista_clase_gratis')


def denegar_clase_gratis(request, clase_id):
    # Obtener la clase gratuita
    clase = get_object_or_404(Clase_Gratis, id=clase_id)
    
    # Cambiar el estado a aceptado
    clase.estado = 'denegado'
    clase.save()
    
    # Enviar un correo electrónico de notificación
    send_mail(
        'Solicitud de clase gratuita denegada',
        'Tu solicitud de clase gratuita ha sido denegada.',
        'from@example.com', 
        [clase.correo],
        fail_silently=False,
    )
    
    # Agregar un mensaje de éxito
    messages.success(request, 'La solicitud ha sido denegada y se ha enviado un correo electrónico al solicitante.')
    
    # Redirigir a la lista de solicitudes
    return redirect('lista_clase_gratis')