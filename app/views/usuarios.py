''' from django.shortcuts import render,redirect
from django.contrib.auth.models import User,Group
from django.contrib import messages
from django.db.models import Q
from app.models import Sede


def listaUsuarios(request):
    usuarios = User.objects.filter(is_superuser=False).values('id', 'username', 'groups__name')
    grupos = Group.objects.all() 
    contexto= {'usuarios':usuarios,'grupos':grupos}
    return render(request, 'app/usuarios/lista_usuarios.html',contexto)





def add_usuario(request):
    
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        contraseña = request.POST.get('contraseña')
  
        nuevo_usuario = User.objects.create_user(username=usuario, password=contraseña)
        user_id = nuevo_usuario.id
        user_group = User.objects.get(id=user_id)
        nombre_grupo = request.POST.get('grupo')
        grupo_objeto = Group.objects.get(name=nombre_grupo)
        user_group.groups.add(grupo_objeto)
        id_sede= int(request.POST.get('id_sede'))
        sede=Sede.objects.get(pk=id_sede)
        sedeusuario= SedeUsuario(usuario=user_group,sede=sede)
        sedeusuario.save()
        messages.success(request,'Usuario Registrado con exito')
        return render(request,'app/usuarios/registrar_usuario.html')
    else:
        grupos = Group.objects.all() 
        sedes = Sede.objects.all()
        contexto={'grupos':grupos,'sedes':sedes}
        return render(request,'app/usuarios/registrar_usuario.html',contexto)
    
def editar_usuario(request,id_usuario):
    usuario= User.objects.get(id=id_usuario)
    if request.method=='POST':
        usuario.username = request.POST.get('usuario')
        nueva_contraseña= request.POST.get('contraseña')
        if nueva_contraseña:
            usuario.set_password(nueva_contraseña)
        
        nombre_grupo = request.POST.get('grupo')
        if nombre_grupo:
            grupo_objeto = Group.objects.get(name=nombre_grupo)
            usuario.groups.clear()  # Eliminar los grupos anteriores
            usuario.groups.add(grupo_objeto)  # Asignar el nuevo grupo
        
        usuario.save()
        messages.success(request, 'Usuario actualizado con éxito')
        return redirect('editar_usuario', id_usuario=usuario.pk)
    else:
        grupos = Group.objects.all()
        return render(request, 'app/usuarios/editar_usuario.html', {'usuario': usuario, 'grupos': grupos})


def eliminar_usuario(request,id_usuario):
    usuario=User.objects.get(id=id_usuario)
    usuario.delete()
    return redirect('lista_usuarios')

def detalles_usuario(request,id_usuario):
    usuario=User.objects.get(id=id_usuario)
    grupos = Group.objects.all()
    contexto={'usuario':usuario,'grupos':grupos}
    return render(request,'app/usuarios/detalles_usuario.html',contexto)


def filtros_columnas(request):
    query = request.GET.get('q')
    if query:
        # Filtrar usuarios por el nombre de usuario
        usuarios = User.objects.filter(
            Q(username__icontains=query),
            is_superuser=False
        ).values('id', 'username', 'groups__name')
    else:
        # Obtener todos los usuarios (excepto superusuarios)
        usuarios = User.objects.filter(is_superuser=False).values('id', 'username', 'groups__name')
    
    contexto = {'usuarios': usuarios, 'query': query}
    return render(request, 'app/usuarios/lista_usuarios.html', contexto)

    solo es de prueba
'''