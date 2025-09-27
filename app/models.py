from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Sede(models.Model):
    departamento=models.CharField(max_length=50)
    provincia=models.CharField(max_length=50)
    distrito=models.CharField(max_length=50)
    direccion=models.CharField(max_length=50)
    foto_local=models.ImageField(upload_to='imagenes_bd/',null=True,blank=True)
    
    class Meta:
        db_table='Sede'

class Docente(models.Model):

    nombre=models.CharField(max_length=50)
    apellido=models.CharField(max_length=50)
    edad=models.IntegerField()
    dni=models.IntegerField()
    correo=models.CharField(max_length=50)
    telefono=models.IntegerField()
    direccion=models.CharField(max_length=50)
    fecha_nacimiento=models.DateField()
    grado_cinturon=models.CharField(max_length=50)
    foto_perfil= models.ImageField(upload_to='imagenes_bd/',null=True,blank=True)
    genero=models.CharField(max_length=10,default='sin genero')
    id_usuario=models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        db_table='Docente'

class Cinturon(models.Model):
    color_cinturon=models.CharField(max_length=50)
    kup=models.IntegerField()
    dan=models.IntegerField()



class Horario(models.Model):
    frecuencia= models.CharField(max_length=30)
    hora_inicio=models.TimeField()
    hora_fin=models.TimeField()
    grupo=models.CharField(max_length=50)
    aforo= models.IntegerField()
    periodo=models.CharField(max_length=30)
    id_docente=models.ForeignKey(Docente,on_delete=models.SET_NULL,null=True,blank=True)
    id_sede=models.ForeignKey(Sede,on_delete=models.CASCADE)
    
    class Meta:
        db_table='Horario'

class Clase_Gratis(models.Model):
    nombres=models.CharField(max_length=20)
    apellidos=models.CharField(max_length=20)
    edad=models.IntegerField()
    correo=models.EmailField()
    celular=models.IntegerField()
    estado=models.CharField(max_length=20,default='En espera')
    id_horario=models.ForeignKey(Horario,on_delete=models.SET_NULL,null=True,blank=True)
    class Meta:
        db_table='Clase_Gratis'

class Alumno(models.Model):
    nombre=models.CharField(max_length=50)
    apellido=models.CharField(max_length=50)
    edad=models.IntegerField()
    dni=models.IntegerField()
    correo=models.CharField(max_length=50)
    telefono=models.IntegerField()
    direccion=models.CharField(max_length=50)
    fecha_nacimiento=models.DateField()
    grado_cinturon=models.ForeignKey(Cinturon,on_delete=models.SET_NULL,null=True,blank=True)
    foto_perfil= models.ImageField(upload_to='imagenes_bd/',null=True,blank=True)
    genero=models.CharField(max_length=10,default='sin genero')
    id_usuario=models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        db_table='Alumno'

class Matricula(models.Model):
    id_alumno=models.ForeignKey(Alumno,on_delete=models.CASCADE)
    monto=models.IntegerField()
    id_horario = models.ForeignKey(Horario,on_delete=models.SET_NULL,null=True,blank=True)  # Asocia matrícula al horario del alumno
    estado=models.CharField(max_length=20,default='sin pagar')
    comprobante_pago = models.ImageField(upload_to='imagenes_bd/', null=True, blank=True)
    fecha=models.DateField()

class Asistencia(models.Model):
    id_horario = models.ForeignKey('Horario', on_delete=models.CASCADE)  # Clase a la que pertenece la asistencia
    fecha = models.DateTimeField()  # Fecha de la sesión
    
    class Meta:
        db_table='Asistencia'


class Asistencia_alumno(models.Model):
    id_asistencia=models.ForeignKey(Asistencia,on_delete=models.CASCADE)
    id_alumno=models.ForeignKey(Alumno,on_delete=models.CASCADE)
    estado=models.CharField(max_length=10)

    class Meta:
        db_table='Asistencia_alumno'

