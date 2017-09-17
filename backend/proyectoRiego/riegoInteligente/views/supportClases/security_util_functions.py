from datetime import datetime
import pytz

from django.db import transaction
from django.contrib.auth.signals import user_logged_in, user_logged_out

from ...models import SesionUsuario, TipoSesion
from views_util_functions import *
from views_constants import *
from security_parameters import *


# noinspection PyUnusedLocal
@transaction.atomic()
def user_logged_in_handler(sender, request, user, **kwargs):
    datos = obtener_datos_json(request)

    request.session.set_expiry(SESSION_EXPIRATION_TIME)

    sesion_usuario, created = SesionUsuario.objects.get_or_create(
                user=user,
                session_id=request.session.session_key
                )

    sesion_usuario.fecha_y_hora_ultimo_acceso = datetime.now(pytz.utc)
    sesion_usuario.fecha_y_hora_fin = request.session.get_expiry_date()

    if KEY_TIPO_SESION in datos:
        id_tipo_sesion = datos[KEY_TIPO_SESION]
        try:
            tipo_sesion = TipoSesion.objects.get(idTipo=id_tipo_sesion)
            sesion_usuario.tipo_sesion = tipo_sesion
        except TipoSesion.DoesNotExist:
            pass

    if created:
        sesion_usuario.fecha_y_hora_inicio = datetime.now(pytz.utc)
        delete_user_sessions(user, request.session.session_key)

    sesion_usuario.save()


user_logged_in.connect(user_logged_in_handler)


# noinspection PyUnusedLocal
@transaction.atomic()
def user_logged_out_handler(sender, request, user, **kwargs):
    delete_user_sessions(user,"")


user_logged_out.connect(user_logged_out_handler)


@transaction.atomic()
def delete_user_sessions(user, session_key):
    sesiones_usuario = SesionUsuario.objects.filter(user=user).exclude(session_id=None)
    for sesion_usuario in sesiones_usuario:
        if session_key != sesion_usuario.session.session_key:
            sesion_usuario.fecha_y_hora_fin = datetime.now(pytz.utc)
            sesion_usuario.session.delete()
