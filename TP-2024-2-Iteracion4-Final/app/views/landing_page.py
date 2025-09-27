from django.shortcuts import render,redirect
from django.contrib import messages
from app.models import Horario, Sede,Clase_Gratis,Horario
import os
from django.conf import settings

def clase_gratis_landing(request):
    return render(request,'app/landing/clase_gratis.html')

def solicitar_clase_Gratis(request):
    horarios = Horario.objects.all()  # Por defecto, todos los horarios
    sede_seleccionada = request.GET.get('sede')  # Obtener la sede seleccionada del formulario
    if sede_seleccionada:
        
        horarios = horarios.filter(id_sede=sede_seleccionada)
    sedes = Sede.objects.all()
    contexto={'sedes':sedes,'horarios':horarios}
    return render(request,'app/landing/solicitar_clase_Gratis.html',contexto)

def eventos(request):
    return render(request, 'app/landing/eventos.html')

def registrar_clase_gratis(request):
    if request.method == 'POST':
    
        nombres = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')
        edad = int(request.POST.get('edad'))
        correo = request.POST.get('correo')
        celular = request.POST.get('celular')
     
        id_horario = int(request.POST.get('horario'))
        horario = Horario.objects.get(id=id_horario)

        clase_gratis = Clase_Gratis(
            nombres=nombres,
            apellidos=apellidos,
            edad=edad,
            correo=correo,
            celular=celular,
            id_horario=horario
        )


        try:
            clase_gratis.save()
            messages.success(request, "Clase solicitada. Se te notificará por correo la confirmación de la clase.")
        except Exception as e:
            messages.error(request, f"Hubo un error en el registro: {e} Intentar nuevamente")
        
        return redirect('solicitar_clase_gratis')



def Sedes_landing(request):
    sedes = Sede.objects.all()

    # Obtener docentes relacionados con cada sede a través de Horario
    for sede in sedes:
        # Usar un conjunto para eliminar duplicados
        telefonos_set = set(
            '51' + str(docente['id_docente__telefono'])
            for docente in sede.horario_set.all().values('id_docente__telefono')
        )
        # Convertir el conjunto a lista para facilitar su uso en plantillas
        sede.docentes_telefonos = list(telefonos_set)

    return render(request, 'app/landing/Sedes.html', {'sedes': sedes})


def galeria_landing(request):
    image_folder = os.path.join(settings.BASE_DIR, 'app/static/app/img')
    
    # Filtrar imágenes que comiencen con "galeria" seguido de un número
    images = [
        img for img in os.listdir(image_folder) 
        if img.startswith('galeria') and 
           img.split('galeria')[1][0].isdigit() and 
           img.endswith(('.png', '.jpg', '.jpeg', '.gif'))
    ]
    
    return render(request, 'app/landing/galeria.html', {'images': images})

