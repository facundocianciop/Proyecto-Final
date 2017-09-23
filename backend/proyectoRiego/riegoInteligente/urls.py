from django.conf.urls import url

from views import views_modulo_seguridad
from views import views_modulo_finca
from views import views_configuracion_finca
from views import views_configuracion_sectores


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

    url(r'^crearSector/$', views_configuracion_sectores.crearSector, name='crearSector'),
    url(r'^mostrarSectores/$', views_configuracion_sectores.mostrarSectores, name='mostrarSectores'),
    url(r'^asignarMecanismoASector/$', views_configuracion_sectores.asignarMecanismoASector, name = 'asignarMecanismoASector'),
    url(r'^modificarSector/$', views_configuracion_sectores.modificarSector, name = 'modificarSector'),
    url(r'^eliminarSector/$', views_configuracion_sectores.eliminarSector, name = 'eliminarSector'),

    url(r'^mostrarMecanismosRiegoFinca/$', views_configuracion_finca.mostrarMecanismosRiegoFinca, name='mostrarMecanismosRiegoFinca'),
    url(r'^mostrarMecanismosNuevos/$', views_configuracion_finca.mostrarMecanismosNuevos,
        name='mostrarMecanismosNuevos'),
    url(r'^agregarMecanismoRiegoFinca/$', views_configuracion_finca.agregarMecanismoRiegoFinca, name='agregarMecanismoRiegoFinca'),

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