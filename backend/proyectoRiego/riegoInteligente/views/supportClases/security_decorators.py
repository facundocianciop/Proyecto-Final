from datetime import datetime
import pytz
from functools import wraps

from django.http import HttpResponse
from django.utils.decorators import available_attrs

from ...models import SesionUsuario
from error_handler import *


# Controla si el usuario haciendo una llamada esta loggeado
def login_requerido(funcion):

    def wrap(request, *args, **kwargs):
        # verificar que el usuario haciendo la llamada este autenticado
        if request.user.is_authenticated:
            request.session.modified = True
            sesion_usuario = SesionUsuario.objects.get(session_id=request.session.session_key)
            sesion_usuario.fecha_y_hora_ultimo_acceso = datetime.now(pytz.utc)
            sesion_usuario.fecha_y_hora_fin = request.session.get_expiry_date()

            sesion_usuario.save()

            return funcion(request, *args, **kwargs)
        else:
            return build_unauthorized_error(HttpResponse(), ERROR_LOGIN_REQUERIDO, "Usuario no inicio sesion")

    wrap. __doc__ = funcion.__doc__
    wrap. __name__ = funcion.__name__

    return wrap


# Controla si el metodo enviado es correcto
def metodos_requeridos(request_method_list):
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            if request.method not in request_method_list:
                return build_method_not_allowed_error(HttpResponse(), ERROR_METODO_INCORRECTO,
                                                      'Metodo/s requeridod: ' + ', '.join(request_method_list))
            return func(request, *args, **kwargs)
        return inner
    return decorator


# TODO arreglar metodo roles
def permisos_rol_requeridos(permisos_rol_list):
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            """
            Controlar permisos: pasar a un metodo comun
            usuario_finca = mecanismo_riego_finca_sector_seleccionado.mecanismoRiegoFinca.finca.usuariofinca_set.get(
            usuario=request.user.datosusuario
            )

            rol_usuario_finca = usuario_finca.rolUsuarioFincaList.order_by('-fechaAltaRol').first()
            permiso_obtener_riego_en_ejecucion = \
            rol_usuario_finca.conjuntoPermisos.puedeIniciarODetenerRiegoManualmente
            """

            if request.method not in permisos_rol_list:
                return build_method_not_allowed_error(HttpResponse(), ERROR_METODO_INCORRECTO,
                                                      'Metodo/s requeridod: ' + ', '.join(permisos_rol_list))
            return func(request, *args, **kwargs)
        return inner
    return decorator
