from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^sector/$', views.sector, name='sector'),
    url(r'^registrarse/$',views.registrarse,name='registrarse'),
    url(r'^cambiarContrasenia/$', views.cambioContrasenia, name='cambiarContrasenia'),
    url(r'^autenticarse/$', views.autenticarse, name='autenticarse'),
    url(r'^iniciarSesion/$', views.iniciarSesion, name='iniciarSesion')
]