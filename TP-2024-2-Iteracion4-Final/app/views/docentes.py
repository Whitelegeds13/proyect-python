from django.shortcuts import render,redirect
from django.contrib import messages
from app.models import Docente
from app.models import Sede
from django.contrib.auth.models import User,Group
from django.db.models import Q
from datetime import datetime


def lista_docentes(request):
    docentes=Docente.objects.all()
    return render(request,'app/docentes/lista_docentes.html',{'docentes':docentes})

def calcular_edad(fecha_nacimiento):
    hoy = datetime.today().date()  
    edad = hoy.year - fecha_nacimiento.year
    if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
        edad -= 1
    return edad

def registrar_docente(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        contraseña = request.POST.get('contraseña')
        if User.objects.filter(username=usuario).exists():
            messages.error(request, 'El nombre de usuario ya está registrado.')
            return redirect('registrar_docente')

        nuevo_usuario = User.objects.create_user(username=usuario, password=contraseña)
        user_id = nuevo_usuario.id
        user_group = User.objects.get(id=user_id)
        nombre_grupo = request.POST.get('grupo')
        grupo_objeto = Group.objects.get(name=nombre_grupo)
        user_group.groups.add(grupo_objeto)
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        dni = int(request.POST.get('dni'))
        correo = request.POST.get('correo')
        telefono=request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        fecha_nacimiento_str = request.POST.get('fecha_nacimiento')  
        grado_cinturon = request.POST.get('grado_cinturon')
        foto_perfil = request.FILES.get('foto_perfil')
        genero = request.POST.get('genero')
        fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d').date()
        edad = calcular_edad(fecha_nacimiento)
        user_instance = User.objects.get(pk=user_id)
        docente = Docente(
            nombre=nombre,
            apellido=apellido,
            edad=edad,  
            dni=dni,
            correo=correo,
            telefono=telefono,
            direccion=direccion,
            fecha_nacimiento=fecha_nacimiento,  
            grado_cinturon=grado_cinturon,
            foto_perfil=foto_perfil,
            genero=genero,
            id_usuario=user_instance,
        )


        if edad>18 and edad <80:
            docente.save()
            messages.success(request, 'Docente Registrado con exito')
            return redirect("lista_docentes")
        else:
            messages.error(request,'EL profesor debe ser mayor de edad')
            return redirect('registrar_docente')

    else: 
        # Obtener usuarios y grupos
        usuarios = User.objects.filter(is_superuser=False, docente__isnull=True)
        grupos = Group.objects.all()
        contexto = {'usuarios': usuarios, 'grupos': grupos}
        return render(request, 'app/docentes/registrar_docente.html', contexto)
    
def editar_docente(request, id_docente):
    docente = Docente.objects.get(id=id_docente)
    if request.method == 'POST':
        docente.nombre = request.POST.get('nombre')
        docente.apellido = request.POST.get('apellido')

        # Convertir la fecha de nacimiento a un objeto datetime
        fecha_nacimiento_str = request.POST.get('fecha_nacimiento')
        fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d').date()

        # Calcular la edad a partir de la nueva fecha de nacimiento
        docente.edad = calcular_edad(fecha_nacimiento)
        docente.fecha_nacimiento = fecha_nacimiento

        docente.dni = int(request.POST.get('dni'))
        docente.correo = request.POST.get('correo')
        docente.telefono = request.POST.get('telefono')
        docente.direccion = request.POST.get('direccion')
        docente.grado_cinturon = request.POST.get('grado_cinturon')

        # Manejo de la foto de perfil
        if 'foto_perfil' in request.FILES:
            docente.foto_perfil = request.FILES['foto_perfil']

        docente.genero = request.POST.get('genero')
        usuario = int(request.POST.get('usuario'))
        user_instance = User.objects.get(pk=usuario)
        docente.id_usuario = user_instance
        if docente.edad>18 and docente.edad <80:
            docente.save()
            messages.success(request, 'Docente Editado con exito')
            return redirect('lista_docentes')
        else:
            messages.error(request,'EL profesor debe ser mayor de edad')
            return redirect('editar_docente', id_docente )
    else:
        usuarios = User.objects.filter(is_superuser=False, docente__isnull=True)
        contexto = {'usuarios': usuarios, 'docente': docente}
        return render(request, 'app/docentes/editar_docente.html', contexto)

def detalle_docente(request, id_docente):
    docente = Docente.objects.get(id=id_docente)
    return render(request, 'app/docentes/detalle_docente.html', {'docente':docente})

def eliminar_docente(request,id_docente):
    docente=Docente.objects.get(id=id_docente)
    usuario=docente.id_usuario
    usuario.delete()
    return redirect('lista_docentes')

def filtros_columnas(request):
    query = request.GET.get('q')
    if query:
        docentes=Docente.objects.filter(
            Q(id__icontains=query)|
            Q(dni__icontains=query) | 
            Q(nombre__icontains=query) | 
            Q(grado_cinturon__icontains=query)
        )
    else:
        docentes=Docente.objects.all()
    contexto={'docentes':docentes,'query':query}
    return render(request,'app/docentes/lista_docentes.html',contexto)

def filtro_cinta(request):
    query=request.GET.get('q')
    if query:
        docentes=Docente.objects.filter(grado_cinturon__contains=query)
    else:
        docentes=Docente.objects.all()
        contexto={'docentes':docentes,'query':query}
        return render(request,'app/docentes/lista_docentes.html',contexto)

