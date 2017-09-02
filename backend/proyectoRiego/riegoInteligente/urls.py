from django.conf.urls import url

from riegoInteligente.views import viewsSeguridad
from riegoInteligente.views import viewsFinca

urlpatterns = [
    url(r'^index/$', viewsFinca.index, name='index'),
    url(r'^sector/$', viewsFinca.sector, name='sector'),
    url(r'^registrarse/$', viewsSeguridad.registrarse, name='registrarse'),
    # url(r'^cambiarContrasenia/$', viewsSeguridad.cambioContrasenia, name='cambiarContrasenia'),
    url(r'^autenticarse/$', viewsSeguridad.autenticarse, name='autenticarse'),
    url(r'^iniciarSesion/$', viewsSeguridad.iniciarSesion, name='iniciarSesion'),
    url(r'^cambioContrasenia/$',viewsSeguridad.cambioContrasenia,name='cambioContrasenia')
]