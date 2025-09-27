from django.shortcuts import render,redirect
from django.contrib import messages
from app.models import Sede
from django.db.models import Q

def lista_sedes(request):
    sedes= Sede.objects.all()
    total_sedes=len(sedes)
    contexto ={'sedes':sedes,'total_sedes':total_sedes}
    return render(request,'app/sedes/lista_sedes.html',contexto)

def editar_sedes(request,id_sede):
    sede= Sede.objects.get(id=id_sede)
    if request.method=='POST':
        sede.departamento = request.POST.get('departamento')
        sede.provincia = request.POST.get('provincia')
        sede.distrito = request.POST.get('distrito')
        sede.direccion = request.POST.get('direccion')
        if 'foto_local' in request.FILES:
            sede.foto_local = request.FILES['foto_local']
        
        # Guardar los cambios en la base de datos

        sede.save()
        
        messages.success(request,'Editado con exito')
        return redirect('lista_sedes')
    else:
        return render(request,'app/sedes/editar_sede.html',{'sede':sede})
    
def registrar_sede(request):
    if request.method == 'POST':
        departamento = request.POST.get('departamento')
        provincia = request.POST.get('provincia')
        distrito = request.POST.get('distrito')
        direccion = request.POST.get('direccion')
        foto_local = request.FILES.get('foto_local')

        errors = {}

        # Validaciones de campos vacíos
        if not departamento:
            errors['departamento'] = "Debe seleccionar un departamento."
        if not provincia:
            errors['provincia'] = "Debe seleccionar una provincia."
        if not distrito:
            errors['distrito'] = "Debe ingresar un distrito."
        if not direccion:
            errors['direccion'] = "Debe ingresar una dirección."
        if not foto_local:
            errors['foto_local'] = "Debe subir una foto del local."

        # Verificar duplicados si no hay errores previos
        if not errors:
            if Sede.objects.filter(
                departamento=departamento,
                provincia=provincia,
                distrito=distrito,
                direccion=direccion
            ).exists():
                errors['duplicado'] = "La sede ya existe."

        # Si hay errores, renderizar nuevamente el formulario
        if errors:
            for error in errors.values():
                messages.error(request, error)
            return render(request, 'app/sedes/registrar_sede.html', {
                'departamento': departamento,
                'provincia': provincia,
                'distrito': distrito,
                'direccion': direccion,
                'foto_local': foto_local
            })

        # Intentar guardar la sede
        try:
            sede = Sede(
                departamento=departamento,
                provincia=provincia,
                distrito=distrito,
                direccion=direccion,
                foto_local=foto_local
            )
            sede.save()
            messages.success(request, "Sede registrada con éxito.")
        except Exception as e:
            messages.error(request, f"Hubo un error al registrar la sede: {e}")

        return redirect('lista_sedes')

    return render(request, 'app/sedes/registrar_sede.html')

def detalles_sede(request,id_sede):
    sede=Sede.objects.get(id=id_sede)
    return render(request,'app/sedes/detalles_sede.html',{'sede':sede})

def eliminar_sede(request,id_sede):
    sede=Sede.objects.get(id=id_sede)
    sede.delete()
    messages.success(request,'Sede Eliminada con Exito')
    return redirect('lista_sedes')

def filtros_columnas(request):
    query = request.GET.get('q')
    if query:
        sedes=Sede.objects.filter(
            Q(departamento__icontains=query)|
            Q(provincia__icontains=query) | 
            Q(distrito__icontains=query) | 
            Q(direccion__icontains=query)
        )
    else:
        sedes=Sede.objects.all()
    contexto={'sedes':sedes,'query':query}
    return render(request,'app/sedes/lista_sedes.html',contexto)
