from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def login_admin(request):
    if request.method=='POST':
        usuario=request.POST.get('usuario')
        password=request.POST.get('password')
        user = authenticate(username=usuario, password=password)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('dashboard_admin')
            else:
                return redirect('login_admin')
        elif user is None:
            return redirect('login_admin')
            
    else:
        return render(request,'app/login/login_admin.html')
    
def login_docente(request):
    if request.method == 'POST':
        usuario = request.POST["usuario"]
        password = request.POST["password"]
        user = authenticate(request, username=usuario, password=password)
        
        if user is not None:
            grupos_del_usuario = user.groups.all()
            if user.is_superuser:
                messages.error(request, 'Debe ser un Docente o Alumno')
                return redirect('login')
            elif grupos_del_usuario.filter(name='Docente').exists():
                login(request, user)  
                return redirect('dashboard_docente')
            elif grupos_del_usuario.filter(name='Alumno').exists():
                login(request, user)  
                return redirect('dashboard_alumno')
        
      
        messages.error(request, 'Credenciales incorrectas o usuario no autorizado')
        return redirect('login')
    
    return render(request, 'app/login/login.html')
    
def logout(request):
    request.session.clear()
    return redirect('clase_gratis_landing')

  