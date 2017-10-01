from django.conf.urls import url

from views import views_modulo_seguridad
from views import views_modulo_finca
from views import views_configuracion_finca
from views import views_configuracion_sectores
from views import views_modulo_sensores
from views import views_obtencion_informacion_externa



urlpatterns = [
    url(r'^crearFinca/$', views_modulo_finca.crear_finca, name='crearFinca'),
    url(r'^obtenerFincasEstadoPendiente/$', views_modulo_finca.obtener_fincas_estado_pendiente, name='obtenerFincasEstadoPendiente'),
    url(r'^elegirProveedorInformacion/$', views_modulo_finca.elegir_proveedor_informacion, name='elegirProveedorInformacion'),
    url(r'^buscarProveedoresInformacion/$', views_modulo_finca.buscar_proveedores_informacion, name='buscarProveedoresInformacion'),
    url(r'^obtenerFincasPorUsuario/$', views_modulo_finca.obtener_fincas_por_usuario, name='obtenerFincasPorUsuario'),
    url(r'^aprobarFinca/$', views_modulo_finca.aprobar_finca, name='aprobarFinca'),
    url(r'^noAprobarFinca/$', views_modulo_finca.no_aprobar_finca, name='noAprobarFinca'),
    url(r'^mostrarFincasEncargado/$', views_modulo_finca.mostrar_fincas_encargado, name='mostrarFincasEncargado'),
    url(r'^buscarUsuariosNoEncargado/$', views_modulo_finca.buscar_usuarios_no_encargado, name='buscarUsuariosNoEncargado'),
    url(r'^eliminarUsuarioFinca/$', views_modulo_finca.eliminar_usuario_finca,name='eliminarUsuarioFinca'),
    url(r'^buscarUsuariosNoFinca/$', views_modulo_finca.buscar_usuarios_no_finca, name='buscarUsuariosNoFinca'),
    url(r'^agregarUsuarioFinca/$', views_modulo_finca.agregar_usuario_finca, name='agregarUsuarioFinca'),
    url(r'^modificarRolUsuario/$', views_modulo_finca.modificar_rol_usuario, name='modificarRolUsuario'),
    url(r'^modificarFinca/$', views_modulo_finca.modificar_finca, name='modificarFinca'),
    url(r'^eliminarFinca/$', views_modulo_finca.eliminar_finca, name='eliminarFinca'),

    url(r'^buscarFincaId/$', views_modulo_finca.buscar_finca_id, name='buscarFincaId'),
    url(r'^devolverPermisos/$', views_modulo_finca.devolver_permisos, name='devolverPermisos'),

    url(r'^crearSector/$', views_configuracion_sectores.crear_sector, name='crearSector'),
    url(r'^mostrarSectores/$', views_configuracion_sectores.mostrar_sectores, name='mostrarSectores'),
    url(r'^asignarMecanismoASector/$', views_configuracion_sectores.asignar_mecanismo_a_sector, name ='asignarMecanismoASector'),
    url(r'^mostrarMecanismoRiegoSector/$', views_configuracion_sectores.mostrar_mecanismo_riego_sector, name ='mostrarMecanismoRiegoSector'),
    url(r'^modificarSector/$', views_configuracion_sectores.modificar_sector, name ='modificarSector'),
    url(r'^eliminarSector/$', views_configuracion_sectores.eliminar_sector, name ='eliminarSector'),
    url(r'^deshabilitarMecanismoRiegoSector/$', views_configuracion_sectores.deshabilitar_mecanismo_riego_sector, name ='deshabilitarMecanismoRiegoSector'),
    url(r'^mostrarSubtiposTiposCultivos/$', views_configuracion_sectores.mostrar_subtipos_tipos_cultivos, name ='mostrarSubtiposTiposCultivos'),
    url(r'^asignarCultivoASector/$', views_configuracion_sectores.asignar_cultivo_a_sector, name ='asignarCultivoASector'),
    url(r'^deshabilitarCultivoSector/$', views_configuracion_sectores.deshabilitar_cultivo_sector,
        name='deshabilitarCultivoSector'),
    url(r'^modificarCultivoSector/$', views_configuracion_sectores.modificar_cultivo_sector,
        name='modificarCultivoSector'),
    url(r'^mostrarCultivoSector/$', views_configuracion_sectores.mostrar_cultivo_sector,
        name='mostrarCultivoSector'),
    url(r'^mostrarCultivoSectorHistorico/$', views_configuracion_sectores.mostrar_cultivo_sector_historico,
        name='mostrarCultivoSectorHistorico'),
    url(r'^asignarComponenteSensor/$', views_configuracion_sectores.asignar_componente_sensor, name='asignarComponenteSensor'),
    url(r'^desasignarComponenteSensor/$', views_configuracion_sectores.desasignar_componente_sensor,
        name='desasignarComponenteSensor'),

    url(r'^mostrarMecanismosRiegoFinca/$', views_configuracion_finca.mostrarMecanismosRiegoFinca, name='mostrarMecanismosRiegoFinca'),
    url(r'^mostrarMecanismosNuevos/$', views_configuracion_finca.mostrar_mecanismos_nuevos,
        name='mostrarMecanismosNuevos'),
    url(r'^agregarMecanismoRiegoFinca/$', views_configuracion_finca.agregar_mecanismo_riego_finca, name='agregarMecanismoRiegoFinca'),
    url(r'^deshabilitarMecanismoRiegoFinca/$', views_configuracion_finca.deshabilitar_mecanismo_riego_finca,
        name='deshabilitarMecanismoRiegoFinca'),
    url(r'^habilitarMecanismoRiegoFinca/$', views_configuracion_finca.habilitar_mecanismo_riego_finca,
        name='habilitarMecanismoRiegoFinca'),

    url(r'^crearSensor/$', views_modulo_sensores.crear_sensor, name='crearSensor'),
    url(r'^deshabilitarSensor/$', views_modulo_sensores.deshabilitar_sensor, name='deshabilitarSensor'),
    url(r'^modificarSensor/$', views_modulo_sensores.modificar_sensor, name='modificarSensor'),
    url(r'^buscarSensoresNoAsignados/$', views_modulo_sensores.buscar_sensores_no_asignados, name='buscarSensoresNoAsignados'),

    url(r'^crearComponenteSensor/$', views_modulo_sensores.crear_componente_sensor, name='crearComponenteSensor'),
    url(r'^modificarComponenteSensor/$', views_modulo_sensores.modificar_componente_sensor,
        name='modificarComponenteSensor'),
    url(r'^habilitarComponenteSensor/$', views_modulo_sensores.habilitar_componente_sensor, name='habilitarComponenteSensor'),
    url(r'^deshabilitarComponenteSensor/$', views_modulo_sensores.deshabilitar_componente_sensor, name='deshabilitarComponenteSensor'),
    url(r'^asignarSensorAComponenteSensor/$', views_modulo_sensores.asignar_sensor_a_componente_sensor, name='asignarSensorAComponenteSensor'),
    url(r'^desasignarSensorDeComponenteSensor/$', views_modulo_sensores.desasignar_sensor_de_componente_sensor, name='desasignarSensorDeComponenteSensor'),
    url(r'^mostrarComponentesSensorFinca/$', views_modulo_sensores.mostrar_componentes_sensor_finca, name='mostrarComponentesSensorFinca'),
    url(r'^mostrarComponentesSensorFincaHabilitados/$', views_modulo_sensores.mostrar_componentes_sensor_finca_habilitados, name='mostrarComponentesSensorFincaHabilitados'),
    url(r'^mostrarComponentesSensorFincaNoAsignados/$', views_modulo_sensores.mostrar_componentes_sensor_finca_no_asignados, name='mostrarComponentesSensorFincaNoAsignados'),

    url(r'^mostrarTipoMedicion/$', views_modulo_sensores.mostrar_tipo_medicion, name='mostrarTipoMedicion'),
    url(r'^mostrarSensoresFinca/$', views_modulo_sensores.mostrar_sensores_finca, name='mostrarSensoresFinca'),

    url(r'^obtenerProveedorFinca/$', views_obtencion_informacion_externa.obtener_proveedor_finca, name='obtenerProveedorFinca'),
    url(r'^modificarProveedorFinca/$', views_obtencion_informacion_externa.modificar_proveedor_finca, name='modificarProveedorFinca'),
    url(r'^deshabilitarProveedorFinca/$', views_obtencion_informacion_externa.deshabilitar_proveedor_finca, name='deshabilitarProveedorFinca'),
    url(r'^cambiarProveedorFinca/$', views_obtencion_informacion_externa.cambiar_proveedor_finca, name='cambiarProveedorFinca'),

    url(r'^registrarse/$', views_modulo_seguridad.registrar_usuario, name='registrarse'),
    url(r'^iniciarSesion/$', views_modulo_seguridad.iniciar_sesion, name='iniciarSesion'),
    url(r'^mostrarUsuario/$', views_modulo_seguridad.mostrar_usuario, name='mostrarUsuario'),
    url(r'^cambiarContrasenia/$', views_modulo_seguridad.cambiar_contrasenia, name='cambiarContrasenia'),
    url(r'^cambiarContraseniaRecuperarCuenta/$', views_modulo_seguridad.cambiar_contrasenia_recuperar_cuenta, name='cambiarContraseniaRecuperarCuenta'),
    url(r'^finalizarSesion/$', views_modulo_seguridad.finalizar_sesion, name='finalizarSesion'),
    url(r'^eliminarUsuario/$', views_modulo_seguridad.eliminar_usuario, name='eliminarUsuario'),
    url(r'^modificarUsuario/$', views_modulo_seguridad.modificar_usuario, name='modificarUsuario'),
    url(r'^recuperarCuenta/$', views_modulo_seguridad.recuperar_cuenta, name='recuperarCuenta')
]