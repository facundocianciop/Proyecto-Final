from django.conf.urls import url
from .views import viewsSeguridad
from views import viewsFinca
from views import viewsConfiguracionFinca

urlpatterns = [
    url(r'^index/$', viewsFinca.index, name='index'),
    url(r'^sector/$', viewsFinca.sector, name='sector'),
    url(r'^crearFinca/$', viewsFinca.crearFinca, name='crearFinca'),
    url(r'^obtenerFincasEstadoPendiente/$', viewsFinca.obtenerFincasEstadoPendiente, name='obtenerFincasEstadoPendiente'),
    url(r'^elegirProveedorInformacion/$', viewsFinca.elegirProveedorInformacion, name='elegirProveedorInformacion'),
    url(r'^buscarProveedoresInformacion/$', viewsFinca.buscarProveedoresInformacion, name='buscarProveedoresInformacion'),
    url(r'^obtenerFincasPorUsuario/$',viewsFinca.obtenerFincasPorUsuario,name='obtenerFincasPorUsuario'),
    url(r'^aprobarFinca/$', viewsFinca.aprobarFinca,name='aprobarFinca'),
    url(r'^noAprobarFinca/$', viewsFinca.noAprobarFinca,name='noAprobarFinca'),
    url(r'^mostrarFincasEncargado/$', viewsFinca.mostrarFincasEncargado, name='mostrarFincasEncargado'),
    url(r'^buscarStakeholdersFinca/$', viewsFinca.buscarStakeholdersFinca, name='buscarStakeholdersFinca'),
    url(r'^eliminarStakeholderFinca/$', viewsFinca.eliminarStakeholderFinca,name='eliminarStakeholderFinca'),
    url(r'^buscarUsuarios/$', viewsFinca.buscarUsuarios,name='buscarUsuarios'),
    url(r'^agregarUsuarioFinca/$', viewsFinca.agregarUsuarioFinca,name='agregarUsuarioFinca'),
    url(r'^modificarRolUsuario/$', viewsFinca.modificarRolUsuario, name='modificarRolUsuario'),
    url(r'^modificarFinca/$', viewsFinca.modificarFinca, name='modificarFinca'),

    url(r'^mostrarMecanismosRiegoFinca/$', viewsConfiguracionFinca.mostrarMecanismosRiegoFinca, name='mostrarMecanismosRiegoFinca'),
    url(r'^mostrarMecanismosNuevos/$', viewsConfiguracionFinca.mostrarMecanismosNuevos,
        name='mostrarMecanismosNuevos'),
    url(r'^agregarMecanismoRiegoFinca/$', viewsConfiguracionFinca.agregarMecanismoRiegoFinca, name='agregarMecanismoRiegoFinca'),

    url(r'^registrarse/$', viewsSeguridad.registrarse, name='registrarse'),
    url(r'^iniciarSesion/$', viewsSeguridad.iniciarSesion, name='iniciarSesion'),
    url(r'^mostrarUsuario/$', viewsSeguridad.mostrarUsuario, name='mostrarUsuario'),
    url(r'^cambiarContrasenia/$',viewsSeguridad.cambiarContrasenia,name='cambiarContrasenia'),
    url(r'^finalizarSesion/$', viewsSeguridad.finalizarSesion, name='finalizarSesion'),
    url(r'^eliminarUsuario/$',viewsSeguridad.eliminarUsuario,name='eliminarUsuario'),
    url(r'^modificarUsuario/$',viewsSeguridad.modificarUsuario,name='modificarUsuario'),
    url(r'^recuperarCuenta/$', viewsSeguridad.recuperarCuenta, name='recuperarCuenta')

]