from django.conf.urls import url
from .views import viewsSeguridad
from views import viewsFinca

urlpatterns = [
    url(r'^index/$', viewsFinca.index, name='index'),
    url(r'^sector/$', viewsFinca.sector, name='sector'),
    url(r'^crearFinca/$', viewsFinca.crearFinca, name='crearFinca'),
    url(r'^registrarse/$', viewsSeguridad.registrarse, name='registrarse'),
    url(r'^iniciarSesion/$', viewsSeguridad.iniciarSesion, name='iniciarSesion'),
    url(r'^cambioContrasenia/$',viewsSeguridad.cambioContrasenia,name='cambioContrasenia'),
    url(r'^finalizarSesion/$', viewsSeguridad.finalizarSesion, name='finalizarSesion'),
]