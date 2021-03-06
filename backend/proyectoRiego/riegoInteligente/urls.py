from django.conf.urls import url

from views import views_modulo_seguridad
from views import views_modulo_finca
from views import views_configuracion_finca
from views import views_configuracion_sectores
from views import views_modulo_sensores
from views import views_modulo_reportes

from views import views_obtencion_informacion_externa
from views import views_modulo_interfaz_sensores
from views import views_administrador

from views import views_modulo_configuracion_riego


urlpatterns = [

    url(r'^buscarRoles/$', views_modulo_finca.buscar_roles,
        name='buscarRoles'),

    url(r'^crearFinca/$', views_modulo_finca.crear_finca, name='crearFinca'),
    url(r'^obtenerFincasEstadoPendiente/$', views_modulo_finca.obtener_fincas_estado_pendiente,
        name='obtenerFincasEstadoPendiente'),
    url(r'^buscarProveedoresInformacion/$', views_modulo_finca.buscar_proveedores_informacion,
        name='buscarProveedoresInformacion'),
    url(r'^buscarProveedorNombre/$', views_obtencion_informacion_externa.buscar_proveedor_nombre,
        name='buscarProveedorNombre'),
    url(r'^buscarUltimaMedicion/$', views_obtencion_informacion_externa.buscar_ultima_medicion,
        name='buscarUltimaMedicion'),
    url(r'^obtenerFincasPorUsuario/$', views_modulo_finca.obtener_fincas_por_usuario,
        name='obtenerFincasPorUsuario'),
    url(r'^mostrarFincasEncargado/$', views_modulo_finca.mostrar_fincas_encargado, name='mostrarFincasEncargado'),
    url(r'^buscarUsuariosNoEncargado/$', views_modulo_finca.buscar_usuarios_no_encargado,
        name='buscarUsuariosNoEncargado'),
    url(r'^eliminarUsuarioFinca/$', views_modulo_finca.eliminar_usuario_finca, name='eliminarUsuarioFinca'),
    url(r'^buscarUsuariosFinca/$', views_modulo_finca.buscar_usuarios_finca, name='buscarUsuariosFinca'),
    url(r'^buscarUsuariosNoFinca/$', views_modulo_finca.buscar_usuarios_no_finca, name='buscarUsuariosNoFinca'),
    url(r'^agregarUsuarioFinca/$', views_modulo_finca.agregar_usuario_finca, name='agregarUsuarioFinca'),
    url(r'^modificarRolUsuario/$', views_modulo_finca.modificar_rol_usuario, name='modificarRolUsuario'),
    url(r'^modificarFinca/$', views_modulo_finca.modificar_finca, name='modificarFinca'),
    url(r'^eliminarFinca/$', views_modulo_finca.eliminar_finca, name='eliminarFinca'),
    url(r'^rehabilitarFinca/$', views_modulo_finca.rehabilitar_finca, name='rehabilitarFinca'),


    url(r'^buscarFincaId/$', views_modulo_finca.buscar_finca_id, name='buscarFincaId'),
    url(r'^buscarUsuarioFincaId/$', views_modulo_finca.buscar_usuario_finca_id, name='buscarUsuarioFincaId'),

    url(r'^devolverPermisos/$', views_modulo_finca.devolver_permisos, name='devolverPermisos'),

    url(r'^crearSector/$', views_configuracion_sectores.crear_sector, name='crearSector'),
    url(r'^mostrarSectores/$', views_configuracion_sectores.mostrar_sectores, name='mostrarSectores'),
    url(r'^buscarSectorId/$', views_configuracion_sectores.buscar_sector_id, name='buscarSectorId'),

    url(r'^asignarMecanismoASector/$', views_configuracion_sectores.asignar_mecanismo_a_sector,
        name='asignarMecanismoASector'),
    url(r'^mostrarMecanismoRiegoSector/$', views_configuracion_sectores.mostrar_mecanismo_riego_sector,
        name='mostrarMecanismoRiegoSector'),
    url(r'^mostrarComponenteSensorSector/$', views_configuracion_sectores.mostrar_componente_sensor_sector,
        name='mostrarComponenteSensorSector'),
    url(r'^modificarSector/$', views_configuracion_sectores.modificar_sector, name='modificarSector'),
    url(r'^eliminarSector/$', views_configuracion_sectores.eliminar_sector, name='eliminarSector'),
    url(r'^deshabilitarMecanismoRiegoSector/$', views_configuracion_sectores.deshabilitar_mecanismo_riego_sector,
        name='deshabilitarMecanismoRiegoSector'),
    url(r'^mostrarSubtiposTiposCultivos/$', views_configuracion_sectores.mostrar_subtipos_tipos_cultivos,
        name='mostrarSubtiposTiposCultivos'),
    url(r'^asignarCultivoASector/$', views_configuracion_sectores.asignar_cultivo_a_sector,
        name='asignarCultivoASector'),
    url(r'^deshabilitarCultivoSector/$', views_configuracion_sectores.deshabilitar_cultivo_sector,
        name='deshabilitarCultivoSector'),
    url(r'^modificarCultivoSector/$', views_configuracion_sectores.modificar_cultivo_sector,
        name='modificarCultivoSector'),
    url(r'^mostrarCultivoSector/$', views_configuracion_sectores.mostrar_cultivo_sector,
        name='mostrarCultivoSector'),
    url(r'^buscarCultivoId/$', views_configuracion_sectores.buscar_cultivo_id,
        name='buscarCultivoId'),
    url(r'^mostrarCultivoSectorHistorico/$', views_configuracion_sectores.mostrar_cultivo_sector_historico,
        name='mostrarCultivoSectorHistorico'),
    url(r'^buscarSensoresComponente/$', views_modulo_sensores.buscar_sensores_componente,
        name='buscarSensoresComponente'),
    url(r'^asignarComponenteSensor/$', views_configuracion_sectores.asignar_componente_sensor,
        name='asignarComponenteSensor'),
    url(r'^buscarComponenteSensorPorId/$', views_modulo_sensores.buscar_componente_sensor_por_id,
        name='buscarComponenteSensorPorId'),
    url(r'^desasignarComponenteSensor/$', views_configuracion_sectores.desasignar_componente_sensor,
        name='desasignarComponenteSensor'),

    url(r'^mostrarMecanismosRiegoFinca/$', views_configuracion_finca.mostrarMecanismosRiegoFinca,
        name='mostrarMecanismosRiegoFinca'),


    url(r'^mostrarMecanismosNuevos/$', views_configuracion_finca.mostrar_mecanismos_nuevos,
        name='mostrarMecanismosNuevos'),
    url(r'^agregarMecanismoRiegoFinca/$', views_configuracion_finca.agregar_mecanismo_riego_finca,
        name='agregarMecanismoRiegoFinca'),
    url(r'^deshabilitarMecanismoRiegoFinca/$', views_configuracion_finca.deshabilitar_mecanismo_riego_finca,
        name='deshabilitarMecanismoRiegoFinca'),
    url(r'^habilitarMecanismoRiegoFinca/$', views_configuracion_finca.habilitar_mecanismo_riego_finca,
        name='habilitarMecanismoRiegoFinca'),

    url(r'^crearSensor/$', views_modulo_sensores.crear_sensor, name='crearSensor'),
    url(r'^buscarSensorId/$', views_modulo_sensores.buscar_sensor_id, name='buscarSensorId'),
    url(r'^deshabilitarSensor/$', views_modulo_sensores.deshabilitar_sensor, name='deshabilitarSensor'),
    url(r'^modificarSensor/$', views_modulo_sensores.modificar_sensor, name='modificarSensor'),
    url(r'^buscarSensoresNoAsignados/$', views_modulo_sensores.buscar_sensores_no_asignados,
        name='buscarSensoresNoAsignados'),

    url(r'^crearComponenteSensor/$', views_modulo_sensores.crear_componente_sensor, name='crearComponenteSensor'),
    url(r'^modificarComponenteSensor/$', views_modulo_sensores.modificar_componente_sensor,
        name='modificarComponenteSensor'),
    url(r'^habilitarComponenteSensor/$', views_modulo_sensores.habilitar_componente_sensor,
        name='habilitarComponenteSensor'),
    url(r'^deshabilitarComponenteSensor/$', views_modulo_sensores.deshabilitar_componente_sensor,
        name='deshabilitarComponenteSensor'),
    url(r'^asignarSensorAComponenteSensor/$', views_modulo_sensores.asignar_sensor_a_componente_sensor,
        name='asignarSensorAComponenteSensor'),
    url(r'^desasignarSensorDeComponenteSensor/$', views_modulo_sensores.desasignar_sensor_de_componente_sensor,
        name='desasignarSensorDeComponenteSensor'),
    url(r'^mostrarComponentesSensorFinca/$', views_modulo_sensores.mostrar_componentes_sensor_finca,
        name='mostrarComponentesSensorFinca'),
    url(r'^mostrarComponentesSensorFincaHabilitados/$',
        views_modulo_sensores.mostrar_componentes_sensor_finca_habilitados,
        name='mostrarComponentesSensorFincaHabilitados'),
    url(r'^mostrarComponentesSensorFincaNoAsignados/$',
        views_modulo_sensores.mostrar_componentes_sensor_finca_no_asignados,
        name='mostrarComponentesSensorFincaNoAsignados'),

    url(r'^mostrarTipoMedicion/$', views_modulo_sensores.mostrar_tipo_medicion, name='mostrarTipoMedicion'),
    url(r'^mostrarSensoresFinca/$', views_modulo_sensores.mostrar_sensores_finca, name='mostrarSensoresFinca'),

    url(r'^obtenerProveedorFinca/$', views_obtencion_informacion_externa.obtener_proveedor_finca,
        name='obtenerProveedorFinca'),
    url(r'^modificarProveedorFinca/$', views_obtencion_informacion_externa.modificar_proveedor_finca,
        name='modificarProveedorFinca'),
    url(r'^deshabilitarProveedorFinca/$', views_obtencion_informacion_externa.deshabilitar_proveedor_finca,
        name='deshabilitarProveedorFinca'),
    url(r'^cambiarProveedorFinca/$', views_obtencion_informacion_externa.cambiar_proveedor_finca,
        name='cambiarProveedorFinca'),

    url(r'^registrarse/$', views_modulo_seguridad.registrar_usuario, name='registrarse'),
    url(r'^iniciarSesion/$', views_modulo_seguridad.iniciar_sesion, name='iniciarSesion'),
    url(r'^mostrarUsuario/$', views_modulo_seguridad.mostrar_usuario, name='mostrarUsuario'),
    url(r'^cambiarContrasenia/$', views_modulo_seguridad.cambiar_contrasenia, name='cambiarContrasenia'),
    url(r'^cambiarContraseniaRecuperarCuenta/$', views_modulo_seguridad.cambiar_contrasenia_recuperar_cuenta,
        name='cambiarContraseniaRecuperarCuenta'),
    url(r'^finalizarSesion/$', views_modulo_seguridad.finalizar_sesion, name='finalizarSesion'),
    url(r'^eliminarUsuario/$', views_modulo_seguridad.eliminar_usuario, name='eliminarUsuario'),
    url(r'^modificarUsuario/$', views_modulo_seguridad.modificar_usuario, name='modificarUsuario'),
    url(r'^recuperarCuenta/$', views_modulo_seguridad.recuperar_cuenta, name='recuperarCuenta'),

    url(r'^obtenerRiegoEnEjecucionMecanismoRiegoFincaSector/$',
        views_modulo_configuracion_riego.obtener_riego_en_ejecucion_mecanismo_riego_finca_sector,
        name='obtenerRiegoEnEjecucionMecanismoRiegoFincaSector'),
    url(r'^iniciarRiegoManualmente/$', views_modulo_configuracion_riego.iniciar_riego_manualente,
        name='iniciarRiegoManualmente'),
    url(r'^pausarRiegoManualmente/$', views_modulo_configuracion_riego.pausar_riego_manualente,
        name='pausarRiegoManualmente'),
    url(r'^cancelarRiegoManualmente/$', views_modulo_configuracion_riego.cancelar_riego_manualente,
        name='cancelarRiegoManualmente'),
    url(r'^buscarConfiguracionRiegoId/$',
        views_modulo_configuracion_riego.buscar_configuracion_riego_id,
        name='buscarConfiguracionRiegoId'),
    url(r'^buscarCriterioId/$',
        views_modulo_configuracion_riego.buscar_criterio_id,
        name='buscarCriterioId'),
    url(r'^obtenerConfiguracionesRiegoMecanismoRiegoFincaSector/$',
        views_modulo_configuracion_riego.obtener_configuraciones_riego_mecanismo_riego_finca_sector,
        name='obtenerConfiguracionesRiegoMecanismoRiegoFincaSector'),
    url(r'^obtenerCriteriosInicialesConfiguracionRiegoMecanismoRiegoFincaSector/$',
        views_modulo_configuracion_riego.obtener_criterios_iniciales_configuracion_riego_mecanismo_riego_finca_sector,
        name='obtenerCriteriosInicialesConfiguracionRiegoMecanismoRiegoFincaSector'),
    url(r'^obtenerCriteriosFinalesConfiguracionRiegoMecanismoRiegoFincaSector/$',
        views_modulo_configuracion_riego.obtener_criterios_finales_configuracion_riego_mecanismo_riego_finca_sector,
        name='obtenerCriteriosFinalesConfiguracionRiegoMecanismoRiegoFincaSector'),
    url(r'^crearConfiguracionRiegoAutomaticoMecanismoRiegoFincaSector/$',
        views_modulo_configuracion_riego.crear_configuracion_riego_automatico_mecanismo_riego_finca_sector,
        name='crearConfiguracionRiegoAutomaticoMecanismoRiegoFincaSector'),
    url(r'^crearConfiguracionRiegoManualMecanismoRiegoFincaSector/$',
        views_modulo_configuracion_riego.crear_configuracion_riego_manual_mecanismo_riego_finca_sector,
        name='crearConfiguracionRiegoManualMecanismoRiegoFincaSector'),
    url(r'^cambiarEstadoConfiguracionRiegoMecanismoRiegoFincaSector/$',
        views_modulo_configuracion_riego.cambiar_estado_configuracion_riego_mecanismo_riego_finca_sector,
        name='cambiarEstadoConfiguracionRiegoMecanismoRiegoFincaSector'),
    url(r'^modificarConfiguracionRiegoMecanismoRiegoFincaSector/$',
        views_modulo_configuracion_riego.modificar_configuracion_riego_mecanismo_riego_finca_sector,
        name='modificarConfiguracionRiegoMecanismoRiegoFincaSector'),
    url(r'^eliminarConfiguracionRiegoMecanismoRiegoFincaSector/$',
        views_modulo_configuracion_riego.eliminar_configuracion_riego_mecanismo_riego_finca_sector,
        name='eliminarConfiguracionRiegoMecanismoRiegoFincaSector'),
    url(r'^agregarCriterioInicialConfiguracionRiegoMecanismoRiegoFincaSector/$',
        views_modulo_configuracion_riego.agregar_criterio_inicial_configuracion_riego_mecanismo_riego_finca_sector,
        name='agregarCriterioInicialConfiguracionRiegoMecanismoRiegoFincaSector'),
    url(r'^agregarCriterioFinalConfiguracionRiegoMecanismoRiegoFincaSector/$',
        views_modulo_configuracion_riego.agregar_criterio_final_configuracion_riego_mecanismo_riego_finca_sector,
        name='agregarCriterioFinalConfiguracionRiegoMecanismoRiegoFincaSector'),
    url(r'^eliminarCriterioConfiguracionRiegoMecanismoRiegoFincaSector/$',
        views_modulo_configuracion_riego.eliminar_criterio_configuracion_riego_mecanismo_riego_finca_sector,
        name='eliminarCriterioConfiguracionRiegoMecanismoRiegoFincaSector'),
    url(r'^modificarCriterioConfiguracionRiegoMecanismoRiegoFincaSector/$',
        views_modulo_configuracion_riego.modificar_criterio_configuracion_riego_mecanismo_riego_finca_sector,
        name='modificarCriterioConfiguracionRiegoMecanismoRiegoFincaSector'),

    url(r'^recibirMedicion/$', views_modulo_interfaz_sensores.recibir_medicion,
        name='recibirMedicion'),
    url(r'^buscarConfiguracionesEventosFinca/$',
        views_modulo_reportes.buscar_configuracion_eventos_finca,
        name='buscarConfiguracionesEventosFinca'),
    url(r'^buscarConfiguracionesEventosPersonalizados/$',
        views_modulo_reportes.buscar_configuraciones_eventos_personalizados,
        name='buscarConfiguracionesEventosPersonalizados'),
    url(r'^buscarConfiguracionesEventosPersonalizadosSector/$',
        views_modulo_reportes.buscar_configuraciones_eventos_personalizados_sector,
        name='buscarConfiguracionesEventosPersonalizados'),
    url(r'^mostrarConfiguracionEventoPersonalizado/$',
        views_modulo_reportes.mostrar_configuracion_evento_personalizado,
        name='mostrarConfiguracionEventoPersonalizado'),
    url(r'^buscarTipoMedicionInternaId/$',
        views_modulo_reportes.buscar_tipo_medicion_interna_id,
        name='buscarTipoMedicionInternaId'),
    url(r'^buscarTipoMedicionClimaticaId/$',
        views_modulo_reportes.buscar_tipo_medicion_climatica_id,
        name='buscarTipoMedicionClimaticaId'),
    url(r'^mostrarTipoMedicionInternaFinca/$',
        views_modulo_reportes.mostrar_tipo_medicion_interna_finca,
        name='mostrarTipoMedicionInternaFinca'),
    url(r'^mostrarTipoMedicionClimaticaFinca/$',
        views_modulo_reportes.mostrar_tipo_medicion_climatica_finca,
        name='mostrarTipoMedicionClimaticaFinca'),
    url(r'^crearConfiguracionEventoPersonalizado/$',
        views_modulo_reportes.crear_configuracion_evento_personalizado,
        name='crearConfiguracionEventoPersonalizado'),
    url(r'^asignarConfiguracionEventoPersonalizadoASector/$',
        views_modulo_reportes.asignar_configuracion_evento_personalizado_a_sector,
        name='asignarConfiguracionEventoPersonalizadoASector'),
    url(r'^desasignarConfiguracionEventoPersonalizadoDeSector/$',
        views_modulo_reportes.desasignar_configuracion_evento_personalizado_de_sector,
        name='desasignarConfiguracionEventoPersonalizadoDeSector'),
    url(r'^modificarConfiguracionEventoPersonalizado/$',
        views_modulo_reportes.modificar_configuracion_evento_personalizado,
        name='modifcarConfiguracionEventoPersonalizado'),
    url(r'^desactivarConfiguracionEventoPersonalizado/$',
        views_modulo_reportes.desactivar_configuracion_evento_personalizado,
        name='desactivarConfiguracionEventoPersonalizado'),
    url(r'^activarConfiguracionEventoPersonalizado/$',
        views_modulo_reportes.activar_configuracion_evento_personalizado,
        name='activarConfiguracionEventoPersonalizado'),
    url(r'^obtenerEstadoActualSector/$',
        views_modulo_reportes.obtener_estado_actual_sector,
        name='obtenerEstadoActualSector'),
    url(r'^obtenerInformeRiegoEjecucionSector/$',
        views_modulo_reportes.obtener_informe_riego_ejecucion_sector,
        name='obtenerInformeRiegoEjecucionSector'),
    url(r'^obtenerInformeRiegoHistoricoSector/$',
        views_modulo_reportes.obtener_informe_riego_historico_sector,
        name='obtenerInformeRiegoHistoricoSector'),
    url(r'^obtenerInformeHistoricoSector/$',
        views_modulo_reportes.obtener_informe_historico_sector,
        name='obtenerInformeHistoricoSector'),
    url(r'^obtenerInformeEventosPersonalizados/$',
        views_modulo_reportes.obtener_informe_eventos_personalizados,
        name='obtenerInformeEventosPersonalizados'),
    url(r'^obtenerInformeHistoricoHeladas/$',
        views_modulo_reportes.obtener_informe_historico_heladas,
        name='obtenerInformeHistoricoHeladas'),
    url(r'^obtenerInformeCruzadoRiegoMediciones/$',
        views_modulo_reportes.obtener_informe_cruzado_riego_mediciones_,
        name='obtenerInformeCruzadoRiegoMediciones')
]
