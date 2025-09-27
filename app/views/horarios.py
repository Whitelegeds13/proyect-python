from django.shortcuts import render,redirect
from django.contrib import messages
from app.models import Horario,Sede,Docente
from django.db.models import Q
from datetime import datetime

def lista_Horarios(request):
    horarios=Horario.objects.all()
    return render(request,'app/horarios/lista_horarios.html',{'horarios':horarios})

def registrar_horario(request):
    year = datetime.now().year
    month = datetime.now().month

    if request.method=='POST':
        frecuencia = request.POST.getlist('frecuencia')
        hora_inicio= request.POST.get('hora_inicio')
        hora_Fin = request.POST.get('hora_fin')
        aforo=int(request.POST.get('aforo'))
        grupo= request.POST.get('grupo')
        if month in [1, 2]:  # enero y febrero
            periodo = f"Periodo-{year} Verano"
        else:  # marzo en adelante
            periodo = f"Periodo-{year} Regular"
        id_sede = int(request.POST.get('sede'))
        sede=Sede.objects.get(pk=id_sede)
        id_docente= int(request.POST.get('docente'))
        docente= Docente.objects.get(id=id_docente)

        horario = Horario(frecuencia=frecuencia,hora_inicio=hora_inicio,hora_fin=hora_Fin,grupo=grupo,aforo=aforo,periodo=periodo,id_docente=docente,id_sede=sede )
        try:
            horario.save() 
            messages.success(request, "Registrado con éxito") 
        except Exception as e:
            messages.error(request, "Hubo un error en el registro: {}".format(e))  
        return redirect('lista_horarios')
    else:
        sedes=Sede.objects.all()
        docentes= Docente.objects.all()
        periodo = f"Periodo-{datetime.now().year}"
        if month in [1, 2]:  # enero y febrero
            periodo = f"Periodo-{year} Verano"
        else:  # marzo en adelante
            periodo = f"Periodo-{year} Regular"
        contexto= {'sedes':sedes,'docentes':docentes,'periodo':periodo}
        return render(request,'app/horarios/registrar_horario.html',contexto)
    
def editar_horario(request,id_horario):
    horario= Horario.objects.get(id=id_horario)
    if request.method=='POST':
        horario.frecuencia=request.POST.getlist('frecuencia')
        horario.hora_inicio=request.POST.get('hora_inicio')
        horario.hora_fin = request.POST.get('hora_fin')
        horario.grupo= request.POST.get('grupo')
        horario.aforo = request.POST.get('aforo')
        id_docente= int(request.POST.get('docente'))
        docente=Docente.objects.get(id=id_docente)
        horario.id_docente=docente
        id_sede=int(request.POST.get('sede'))
        sede=Sede.objects.get(id=id_sede)
        horario.id_sede=sede
        try:
            horario.save() 
            messages.success(request, "Registrado con éxito") 
        except Exception as e:
            messages.error(request, "Hubo un error en el registro: {}".format(e))  
        return redirect('lista_horarios')
    else:
        sedes=Sede.objects.all()
        docentes= Docente.objects.all()
        dias = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
        contexto= {'sedes':sedes,'docentes':docentes,'dias':dias,'horario':horario}
        return render(request,'app/horarios/editar_horario.html',contexto)
    
def detalle_horario(request,id_horario):
    horario=Horario.objects.get(id=id_horario)
    dias = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
    contexto= {'dias':dias,'horario':horario}
    return render(request,'app/horarios/detalle_horario.html',contexto)

def eliminar_horario(request,id_horario):
     horario=Horario.objects.get(id=id_horario)
     horario.delete()
     messages.success(request,'Eliminado con exito')
     return redirect('lista_horarios')

def filtros_columnas(request):
    query = request.GET.get('q')
    if query:
        horarios=Horario.objects.filter(
            Q(id__icontains=query)|
            Q(frecuencia__icontains=query) | 
            Q(hora_inicio__icontains=query) | 
            Q(hora_fin__icontains=query)|
            Q(id_docente__nombre__icontains=query)|
            Q(id_sede__departamento__icontains=query)|
            Q(grupo__icontains=query)
        )
    else:
        horarios=Horario.objects.all()
    contexto={'horarios':horarios,'query':query}
    return render(request,'app/horarios/lista_horarios.html',contexto)


