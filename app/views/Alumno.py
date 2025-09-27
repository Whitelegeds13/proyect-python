from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from app.models import Alumno,Cinturon,Docente,Horario,Matricula
from django.contrib.auth.models import User,Group
from django.db.models import Q
from datetime import datetime

def lista_Alumnos(request):
    usuario = request.user
    try:
        # Obtener el docente asociado al usuario autenticado
        docente = Docente.objects.get(id_usuario=usuario)
        
        # Obtener los horarios asociados al docente
        horarios = Horario.objects.filter(id_docente=docente)
        
        # Filtrar las matrículas asociadas a estos horarios
        matriculas = Matricula.objects.filter(id_horario__in=horarios)
        
        # Obtener los alumnos de las matrículas
        alumnos = Alumno.objects.filter(id__in=matriculas.values_list('id_alumno', flat=True))
        
        return render(request, 'app/alumnos/lista_alumnos.html', {'alumnos': alumnos})
    except Docente.DoesNotExist:
        # Manejar el caso donde el usuario no sea un docente
        return render(request, 'app/alumnos/lista_alumnos.html', {'error': 'El usuario no tiene permisos para acceder a esta vista.'})


def calcular_edad(fecha_nacimiento):
    hoy = datetime.today().date()  
    edad = hoy.year - fecha_nacimiento.year
    if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
        edad -= 1
    return edad

def registrar_alumno(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        contraseña = request.POST.get('contraseña')

        # Verificar si el usuario ya existe
        if User.objects.filter(username=usuario).exists():
            messages.error(request, 'El nombre de usuario ya está registrado.')
            return redirect('registrar_alumno')

        # Crear el nuevo usuario
        nuevo_usuario = User.objects.create_user(username=usuario, password=contraseña)
        user_id = nuevo_usuario.id
        user_group = User.objects.get(id=user_id)
        nombre_grupo = request.POST.get('grupo')
        grupo_objeto = Group.objects.get(name=nombre_grupo)
        user_group.groups.add(grupo_objeto)

        # Obtener datos del alumno
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        dni = int(request.POST.get('dni'))
        correo = request.POST.get('correo')
        telefono=request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        fecha_nacimiento_str = request.POST.get('fecha_nacimiento')
        grado_cinturon = int(request.POST.get('grado_cinturon'))
        id_cinturon = Cinturon.objects.get(id=grado_cinturon)
        foto_perfil = request.FILES.get('foto_perfil')
        genero = request.POST.get('genero')
        fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d').date()
        edad = calcular_edad(fecha_nacimiento)

        # Verificar si el alumno tiene una edad válida
        if edad < 3 or edad > 80:
            messages.error(request, 'El alumno debe tener entre 3 y 80 años de edad.')
            return redirect('registrar_alumno')

        # Crear la instancia de Alumno
        alumno = Alumno(
            nombre=nombre,
            apellido=apellido,
            edad=edad,
            dni=dni,
            correo=correo,
            telefono=telefono,
            direccion=direccion,
            fecha_nacimiento=fecha_nacimiento,
            grado_cinturon=id_cinturon,
            foto_perfil=foto_perfil,
            genero=genero,
            id_usuario=nuevo_usuario,  # Asociar al nuevo usuario
        )
        alumno.save()

        # Crear la matrícula
        id_horario = int(request.POST.get('id_horario'))
        horario = Horario.objects.get(id=id_horario)
        monto = int(request.POST.get('monto'))

        matricula = Matricula(
            id_alumno=alumno,
            monto=monto,
            id_horario=horario,
            estado='sin pagar',  # Estado por defecto
            fecha=datetime.today()  # Fecha actual de la matrícula
        )
        matricula.save()

        # Mensaje de éxito y redirección
        messages.success(request, 'Alumno y matrícula registrados con éxito')
        return redirect("lista_alumnos")  # Redirigir a la lista de alumnos

    else:
        # Obtener los datos necesarios para el formulario
        usuarios = User.objects.filter(is_superuser=False, docente__isnull=True)
        grupos = Group.objects.all()
        cinturones = Cinturon.objects.all()
        user_id = request.user.id  # Obtener el ID del usuario que ha iniciado sesión
        docente = Docente.objects.get(id_usuario=user_id)
        horarios = Horario.objects.filter(id_docente=docente.id)

        contexto = {'usuarios': usuarios, 'grupos': grupos, 'cinturones': cinturones, 'horarios': horarios}
        return render(request, 'app/alumnos/registrar_alumno.html', contexto)


def eliminar_alumno(request,id_alumno):
    alumno=Alumno.objects.get(id=id_alumno)
    usuario=alumno.id_usuario
    usuario.delete()
    return redirect('lista_alumnos')

def editar_alumno(request, alumno_id):
    alumno = get_object_or_404(Alumno, id=alumno_id)
    matricula = Matricula.objects.get(id_alumno=alumno)

    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        dni = request.POST.get('dni')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        grado_cinturon_id = request.POST.get('grado_cinturon')
        grado_cinturon = Cinturon.objects.get(id=grado_cinturon_id)
        foto_perfil = request.FILES.get('foto_perfil')
        genero = request.POST.get('genero')

        # Actualizar el alumno
        alumno.nombre = nombre
        alumno.apellido = apellido
        alumno.dni = dni
        alumno.correo = correo
        alumno.telefono = telefono
        alumno.direccion = direccion
        alumno.fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
        alumno.grado_cinturon = grado_cinturon
        alumno.foto_perfil = foto_perfil if foto_perfil else alumno.foto_perfil
        alumno.genero = genero
        alumno.save()

        # No actualizamos el monto

        messages.success(request, 'Datos del alumno actualizados con éxito.')
        return redirect('lista_alumnos')  # Redirigir a la página de detalles del alumno

    # Pasar los datos actuales al formulario
    cinturones = Cinturon.objects.all()

    contexto = {
        'alumno': alumno,
        'matricula': matricula,
        'cinturones': cinturones,
    }

    return render(request, 'app/alumnos/editar_alumno.html', contexto)