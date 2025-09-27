from django.contrib import admin
from .models import Docente,Sede,Cinturon,Horario,Alumno,Matricula,Clase_Gratis
# Register your models here.

admin.site.register(Docente)
admin.site.register(Sede)
admin.site.register(Cinturon)
admin.site.register(Horario)
admin.site.register(Alumno)
admin.site.register(Matricula)
admin.site.register(Clase_Gratis)