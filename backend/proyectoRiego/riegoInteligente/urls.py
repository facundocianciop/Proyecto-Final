from django.conf.urls import url
from .views import views_modulo_seguridad
from views import views_modulo_finca

urlpatterns = [
    url(r'^index/$', views_modulo_finca.index, name='index'),
    url(r'^sector/$', views_modulo_finca.sector, name='sector'),
    url(r'^crearFinca/$', views_modulo_finca.crearFinca, name='crearFinca'),
    url(r'^obtenerFincasEstadoPendiente/$', views_modulo_finca.obtenerFincasEstadoPendiente, name='obtenerFincasEstadoPendiente'),
    url(r'^elegirProveedorInformacion/$', views_modulo_finca.elegirProveedorInformacion, name='elegirProveedorInformacion'),
    url(r'^buscarProveedoresInformacion/$', views_modulo_finca.buscarProveedoresInformacion, name='buscarProveedoresInformacion'),
    url(r'^obtenerFincasPorUsuario/$', views_modulo_finca.obtenerFincasPorUsuario, name='obtenerFincasPorUsuario'),
    url(r'^aprobarFinca/$', views_modulo_finca.aprobarFinca, name='aprobarFinca'),
    url(r'^noAprobarFinca/$', views_modulo_finca.noAprobarFinca, name='noAprobarFinca'),
    url(r'^mostrarFincasEncargado/$', views_modulo_finca.mostrarFincasEncargado, name='mostrarFincasEncargado'),
    url(r'^buscarStakeholdersFinca/$', views_modulo_finca.buscarStakeholdersFinca, name='buscarStakeholdersFinca'),
    url(r'^eliminarStakeholderFinca/$', views_modulo_finca.eliminarStakeholderFinca, name='eliminarStakeholderFinca'),
    url(r'^buscarUsuarios/$', views_modulo_finca.buscarUsuarios, name='buscarUsuarios'),
    url(r'^agregarUsuario/$', views_modulo_finca.agregarUsuario, name='agregarUsuario'),
    url(r'^modificarFinca/$', views_modulo_finca.modificarFinca, name='modificarFinca'),
    url(r'^registrarse/$', views_modulo_seguridad.registrar_usuario, name='registrarse'),
    url(r'^iniciarSesion/$', views_modulo_seguridad.iniciar_sesion, name='iniciarSesion'),
    url(r'^mostrarUsuario/$', views_modulo_seguridad.mostrar_usuario, name='mostrarUsuario'),
    url(r'^cambiarContrasenia/$', views_modulo_seguridad.cambiar_contrasenia, name='cambiarContrasenia'),
    url(r'^finalizarSesion/$', views_modulo_seguridad.finalizar_sesion, name='finalizarSesion'),
    url(r'^eliminarUsuario/$', views_modulo_seguridad.eliminar_usuario, name='eliminarUsuario'),
    url(r'^modificarUsuario/$', views_modulo_seguridad.modificar_usuario, name='modificarUsuario'),
    url(r'^recuperarCuenta/$', views_modulo_seguridad.recuperar_cuenta, name='recuperarCuenta')

]