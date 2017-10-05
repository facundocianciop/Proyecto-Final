# noinspection PyUnresolvedReferences
from datetime import datetime
import pytz

from django.db import transaction
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.core.validators import ValidationError, validate_email
from django.contrib.auth.password_validation import validate_password

from ...models import SesionUsuario, TipoSesion
from views_util_functions import *
from views_constants import *
from security_parameters import *


# noinspection PyUnusedLocal
@transaction.atomic()
def user_logged_in_handler(sender, request, user, **kwargs):
    datos = obtener_datos_json(request)
    tipo_sesion = None

    if user.is_staff:
        # Definir tiempo de sesion para administrador
        request.session.set_expiry(SESSION_EXPIRATION_TIME)
    else:
        # Definir tipo de sesion para otros usuarios
        request.session.set_expiry(ADMIN_USER_SESSION_EXPIRATION_TIME)

        # Controlar que se envie el tipo de sesion
        if KEY_TIPO_SESION in datos:
            id_tipo_sesion = datos[KEY_TIPO_SESION]
        else:
            raise KeyError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_TIPO_SESION_DATOS_FALTANTES)
        if id_tipo_sesion == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_TIPO_SESION_DATOS_FALTANTES)

        try:
            tipo_sesion = TipoSesion.objects.get(idTipo=id_tipo_sesion)
        except TipoSesion.DoesNotExist:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_TIPO_SESION_DATOS_FALTANTES)

    # Busca sesion con usuario y id de sesion, si no encuentra, crea una
    sesion_usuario, created = SesionUsuario.objects.get_or_create(
                user=user,
                session_id=request.session.session_key
                )

    sesion_usuario.fecha_y_hora_ultimo_acceso = datetime.now(pytz.utc)
    sesion_usuario.fecha_y_hora_fin = request.session.get_expiry_date()

    # Si el usuario no es administrador, deberia tener tipo de sesion
    if tipo_sesion is not None:
        sesion_usuario.tipo_sesion = tipo_sesion
        if created:
            sesion_usuario.fecha_y_hora_inicio = datetime.now(pytz.utc)

            # Se eliminan todas las sesiones del mismo tipo
            delete_user_sessions(user, request.session.session_key, tipo_sesion)
    else:
        if created:
            sesion_usuario.fecha_y_hora_inicio = datetime.now(pytz.utc)
            delete_user_sessions(user, request.session.session_key, None)

    sesion_usuario.save()


user_logged_in.connect(user_logged_in_handler)


# noinspection PyUnusedLocal
@transaction.atomic()
def user_logged_out_handler(sender, request, user, **kwargs):
    delete_user_sessions(user, "", None)


user_logged_out.connect(user_logged_out_handler)


@transaction.atomic()
def delete_user_sessions(user, session_key, tipo_sesion):
    if tipo_sesion is not None:
        sesiones_usuario = SesionUsuario.objects.filter(user=user, tipo_sesion=tipo_sesion).exclude(session_id=None)
        for sesion_usuario in sesiones_usuario:
            if session_key != sesion_usuario.session.session_key:
                sesion_usuario.fecha_y_hora_fin = datetime.now(pytz.utc)
                sesion_usuario.session.delete()
    else:
        sesiones_usuario = SesionUsuario.objects.filter(user=user).exclude(session_id=None)
        for sesion_usuario in sesiones_usuario:
            if session_key != sesion_usuario.session.session_key:
                sesion_usuario.fecha_y_hora_fin = datetime.now(pytz.utc)
                sesion_usuario.session.delete()


def validar_contrasenia(password, user):
    try:
        validate_password(password, user=user)
        return True
    except ValidationError:
        return False


def validar_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False
