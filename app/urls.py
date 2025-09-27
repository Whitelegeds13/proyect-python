from django.urls import path
from .views import landing_page ,login,dashboard,sedes,usuarios,docentes,horarios,gestionar_clase_gratis,Perfil_Docente,Alumno,pagos,Perfil_alumno,control_asistencia

urlpatterns = [

    path('',landing_page.clase_gratis_landing,name='clase_gratis_landing'),
    path('login_admin/',login.login_admin,name='login_admin'),
    path('login/',login.login_docente,name='login'),
    path('logout/',login.logout,name='logout'),
    path('dashboard_admin/',dashboard.dashboard_admin,name='dashboard_admin'),
    path('dashboard_docente/',dashboard.dashborad_docente,name='dashboard_docente'),
    path('dashboard_alumno/',dashboard.dashboard_alumno,name='dashboard_alumno'),
    path('Sedes_landing/',landing_page.Sedes_landing,name='Sedes_landing'),
    path('galeria_landing/',landing_page.galeria_landing,name='galeria_landing'),
    path('eventos/', landing_page.eventos, name='eventos'),


    #Sedes
    path('lista_sedes/',sedes.lista_sedes,name='lista_sedes'),
    path('registrar_sede/',sedes.registrar_sede,name='registrar_sede'),
    path('editar_sedes/<int:id_sede>',sedes.editar_sedes,name='editar_sedes'),
    path('detalles_sede/<int:id_sede>',sedes.detalles_sede,name='detalles_sede'),
    path('eliminar_sede/<int:id_sede>',sedes.eliminar_sede,name='eliminar_sede'),

    #Filtros Sede
    path('buscar_sedes/', sedes.filtros_columnas, name='buscar_sedes'),

    path('lista_docentes/',docentes.lista_docentes,name='lista_docentes'),
    path('registrar_docente/',docentes.registrar_docente,name='registrar_docente'),
    path('editar_docente/<int:id_docente>',docentes.editar_docente,name='editar_docente'),
    path('detalles_docente/<int:id_docente>',docentes.detalle_docente,name='detalles_docente'),  
    path('eliminar_docente/<int:id_docente>',docentes.eliminar_docente,name='eliminar_docente'),

    #Filtro Docentes
    path('buscar_docentes/',docentes.filtros_columnas,name='buscar_docentes'),
    path('buscar_cinta',docentes.filtro_cinta,name='filtro_cinta'),

    #horarios
    path('lista_horarios/',horarios.lista_Horarios,name='lista_horarios'),
    path('registrar_horario/',horarios.registrar_horario,name='registrar_horario'),
    path('editar_horario/<int:id_horario>',horarios.editar_horario,name='editar_horario'),
    path('detalle_horario/<int:id_horario>',horarios.detalle_horario,name='detalle_horario'),
    path('eliminar_horario/<int:id_horario>',horarios.eliminar_horario,name='eliminar_horario'),
    # Filtro Horarios
    path('buscar_horarios/', horarios.filtros_columnas, name='buscar_horarios'),

    #Clase Gratis
    path('solicitar_clase_gratis/',landing_page.solicitar_clase_Gratis,name='solicitar_clase_gratis'),
    path('registrar_clase_gratis/',landing_page.registrar_clase_gratis,name='registrar_clase_gratis'),
    path('lista_clase_gratis/',gestionar_clase_gratis.lista_Clase_gratis,name='lista_clase_gratis'),
    path('aceptar-clase-gratis/<int:clase_id>/',gestionar_clase_gratis.aceptar_clase_gratis, name='aceptar_clase_gratis'),
    path('denegar-clase-gratis/<int:clase_id>/', gestionar_clase_gratis.denegar_clase_gratis, name='denegar_clase_gratis'),
    path('editar_perfil/<int:id_docente>/', Perfil_Docente.editar_perfil, name='editar_perfil'),
    path('editar_perfil_alumno/<int:id_alumno>/', Perfil_alumno.editar_perfil_alumno, name='editar_perfil_alumno'),

    #Alumnos

    path('lista_alumnos/',Alumno.lista_Alumnos,name='lista_alumnos'),
    path('registrar_alumno/',Alumno.registrar_alumno,name='registrar_alumno'),
    path('lista_matricula_alumno/',pagos.lista_matricula_alumno,name='lista_matricula_alumno'),
    path('pago_matricula_alumno/<int:matricula_id>/',pagos.pagar_matricula_alumno,name='pago_matricula_alumno'),
    path('eliminar_alumno/<int:id_alumno>',Alumno.eliminar_alumno,name='eliminar_alumno'),
    path('editar_alumno/<int:alumno_id>/', Alumno.editar_alumno,name='editar_alumno'),

    path('lista_evaluar_pago_matricula/',pagos.lista_evaluar_pago_matricula,name='lista_evaluar_pago_matricula'),
    path('aceptar_pago_matricula/<int:matricula_id>',pagos.aceptar_pago_matricula,name='aceptar_pago_matricula'),
    path('denegar_pago_matricula/<int:matricula_id>',pagos.denegar_pago_matricula,name='aceptar_pago_matricula'),

    #Asistencia
    path('control_asistencia/',control_asistencia.control_asistencia,name='control_asistencia'),
    path('lista_control_asistencia/<int:id_horario>',control_asistencia.lista_control_asistencia,name='lista_control_asistencia'),
    path('editar_control_asistencia/<int:id_asistencia>', control_asistencia.editar_control_asistencia,name='editar_control_asistencia'),
    path('miasistencia/',control_asistencia.miAsistenciaAlumno,name='miasistencia'),
]


