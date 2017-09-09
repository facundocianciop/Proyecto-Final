from django.conf.urls import url
from .views import viewsSeguridad
from views import viewsFinca

urlpatterns = [
    url(r'^index/$', viewsFinca.index, name='index'),
    url(r'^sector/$', viewsFinca.sector, name='sector'),
    url(r'^crearFinca/$', viewsFinca.crearFinca, name='crearFinca'),
    url(r'^obtenerFincasEstadoPendiente/$', viewsFinca.obtenerFincasEstadoPendiente, name='obtenerFincasEstadoPendiente'),
    url(r'^elegirProveedorInformacion/$', viewsFinca.elegirProveedorInformacion, name='elegirProveedorInformacion'),
    url(r'^buscarProveedoresInformacion/$', viewsFinca.buscarProveedoresInformacion, name='buscarProveedoresInformacion'),
    url(r'^aprobarFinca/$', viewsFinca.aprobarFinca,name='aprobarFinca'),
    url(r'^noAprobarFinca/$', viewsFinca.noAprobarFinca,name='noAprobarFinca'),
    url(r'^registrarse/$', viewsSeguridad.registrarse, name='registrarse'),
    url(r'^iniciarSesion/$', viewsSeguridad.iniciarSesion, name='iniciarSesion'),
    url(r'^cambiarContrasenia/$',viewsSeguridad.cambiarContrasenia,name='cambiarContrasenia'),
    url(r'^finalizarSesion/$', viewsSeguridad.finalizarSesion, name='finalizarSesion'),
    url(r'^eliminarUsuario/$',viewsSeguridad.eliminarUsuario,name='eliminarUsuario'),
    url(r'^modificarUsuario/$',viewsSeguridad.modificarUsuario,name='modificarUsuario')
]