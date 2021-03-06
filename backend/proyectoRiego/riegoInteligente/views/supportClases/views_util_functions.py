import string
import random
import re

# noinspection PyUnresolvedReferences
from json import loads, dumps
from datetime import datetime
from dateutil import parser
from pytz import timezone, utc

from django.core.mail import EmailMessage
from smtplib import SMTPException, SMTPConnectError, SMTPAuthenticationError
# noinspection PyUnresolvedReferences
from django.core.serializers.json import DjangoJSONEncoder

from views_constants import *
from error_handler import *


def obtener_datos_json(request):
    try:
        received_json_data = str(request.body)
        datos = loads(received_json_data)
        return datos
    except (KeyError, TypeError, ValueError, SystemError, RuntimeError):
        return ""


def armar_response_list_content(lista, *mensaje):
    response_dictionary = {}

    if lista is not None and not len(lista) == 0:

        try:
            response_dictionary[KEY_DATOS_OPERACION] = [item.as_json() for item in lista]
        except (KeyError, TypeError, ValueError, SystemError, RuntimeError):
            response_error_dictionary = {KEY_RESULTADO_OPERACION: False, KEY_DETALLE_OPERACION: DETALLE_ERROR_SISTEMA}
            return dumps(response_error_dictionary, cls=DjangoJSONEncoder)

        if mensaje and len(mensaje) >= 1:
            response_dictionary[KEY_DETALLE_OPERACION] = mensaje[0]
        response_dictionary[KEY_RESULTADO_OPERACION] = True

    else:
        if mensaje and len(mensaje) >= 1:
            response_dictionary[KEY_DETALLE_OPERACION] = mensaje[0]
        else:
            response_dictionary[KEY_DETALLE_OPERACION] = DETALLE_OPERACION_VACIA
        response_dictionary[KEY_RESULTADO_OPERACION] = True

    try:
        return dumps(response_dictionary, cls=DjangoJSONEncoder)
    except (KeyError, TypeError, ValueError, SystemError, RuntimeError):
        response_error_dictionary = {KEY_RESULTADO_OPERACION: False, KEY_DETALLE_OPERACION: DETALLE_ERROR_SISTEMA}
        return dumps(response_error_dictionary, cls=DjangoJSONEncoder)


def armar_response_content(objeto, *mensaje):
    response_dictionary = {}

    if objeto is not None:
        try:
            response_dictionary[KEY_DATOS_OPERACION] = objeto.as_json()
        except (KeyError, TypeError, ValueError, SystemError, RuntimeError):
            response_error_dictionary = {KEY_RESULTADO_OPERACION: False, KEY_DETALLE_OPERACION: DETALLE_ERROR_SISTEMA}
            return dumps(response_error_dictionary, cls=DjangoJSONEncoder)

        if mensaje and len(mensaje) >= 1:
            response_dictionary[KEY_DETALLE_OPERACION] = mensaje[0]
        response_dictionary[KEY_RESULTADO_OPERACION] = True

    else:
        if mensaje and len(mensaje) >= 1:
            response_dictionary[KEY_DETALLE_OPERACION] = mensaje[0]
        else:
            response_dictionary[KEY_DETALLE_OPERACION] = DETALLE_OPERACION_VACIA
        response_dictionary[KEY_RESULTADO_OPERACION] = True

    try:
        return dumps(response_dictionary, cls=DjangoJSONEncoder)
    except (KeyError, TypeError, ValueError, SystemError, RuntimeError):
        response_error_dictionary = {KEY_RESULTADO_OPERACION: False, KEY_DETALLE_OPERACION: DETALLE_ERROR_SISTEMA}
        return dumps(response_error_dictionary, cls=DjangoJSONEncoder)


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def parsear_datos_fecha_a_utc(fecha_string):

    fecha_elegida = parser.parse(fecha_string)

    tz = timezone('America/Argentina/Buenos_Aires')
    datetime_hora_argentina = datetime.now(tz).replace(year=fecha_elegida.year,
                                                       month=fecha_elegida.month,
                                                       day=fecha_elegida.day,
                                                       hour=fecha_elegida.hour,
                                                       minute=fecha_elegida.minute,
                                                       second=fecha_elegida.second
                                                       )
    return datetime_hora_argentina.astimezone(utc)


def parsear_datos_hora_a_utc(hora_string):

    datetime_hora_elegida = parser.parse(hora_string)

    tz = timezone('America/Argentina/Buenos_Aires')
    datetime_hora_argentina = datetime.now(tz).replace(hour=datetime_hora_elegida.hour,
                                                       minute=datetime_hora_elegida.minute,
                                                       second=datetime_hora_elegida.second
                                                       )
    # Convierto la hora a UTC
    return datetime_hora_argentina.astimezone(utc)


# noinspection PyBroadException
def parsear_fecha_a_hora_arg(fecha_utc):
    try:
        tz = timezone('America/Argentina/Buenos_Aires')
        if fecha_utc is not None:
            if isinstance(fecha_utc, datetime):
                return fecha_utc.astimezone(tz)
            else:
                return None
        else:
            return None
    except Exception:
        return None


def validate_regex(expresion_a_evaluar, pattern, detalle_error):
    try:
        pattern = re.compile(pattern=pattern)
        if pattern.match(expresion_a_evaluar) is None:
            raise ValueError(ERROR_VALIDACION_DATOS, detalle_error)

    except re.error:
        raise ValueError(ERROR_VALIDACION_DATOS, detalle_error)


def enviar_email(titulo, mensaje, destino):

    try:
        email = EmailMessage(subject=titulo, body=mensaje, to=[destino])
        email.send()
    except (SMTPException, SMTPConnectError, SMTPAuthenticationError):
        try:
            print "Reintento envio email"
            email = EmailMessage(subject=titulo, body=mensaje, to=[destino])
            email.send()
        except (SMTPException, SMTPConnectError, SMTPAuthenticationError):
            print "Error enviando email"
