import string
import random
# noinspection PyUnresolvedReferences
from json import loads, dumps

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
            response_dictionary = [item.as_json() for item in lista]
        except (KeyError, TypeError, ValueError, SystemError, RuntimeError):
            response_error_dictionary = {KEY_RESULTADO_OPERACION: False}
            response_dictionary[KEY_DETALLE_OPERACION] = DETALLE_ERROR_SISTEMA
            return dumps(response_error_dictionary, cls=DjangoJSONEncoder)

        if mensaje:
            response_dictionary[KEY_DETALLE_OPERACION] = mensaje
        response_dictionary[KEY_RESULTADO_OPERACION] = True

    else:
        if mensaje:
            response_dictionary[KEY_DETALLE_OPERACION] = mensaje
        else:
            response_dictionary[KEY_DETALLE_OPERACION] = DETALLE_OPERACION_VACIA
        response_dictionary[KEY_RESULTADO_OPERACION] = True

    try:
        return dumps(response_dictionary, cls=DjangoJSONEncoder)
    except (KeyError, TypeError, ValueError, SystemError, RuntimeError):
        response_error_dictionary = {KEY_RESULTADO_OPERACION: False}
        response_dictionary[KEY_DETALLE_OPERACION] = DETALLE_ERROR_SISTEMA
        return dumps(response_error_dictionary, cls=DjangoJSONEncoder)


def armar_response_content(objeto, *mensaje):
    response_dictionary = {}

    if objeto is not None:
        try:
            response_dictionary = objeto.as_json()
        except (KeyError, TypeError, ValueError, SystemError, RuntimeError):
            response_error_dictionary = {KEY_RESULTADO_OPERACION: False}
            response_dictionary[KEY_DETALLE_OPERACION] = DETALLE_ERROR_SISTEMA
            return dumps(response_error_dictionary, cls=DjangoJSONEncoder)

        if mensaje:
            response_dictionary[KEY_DETALLE_OPERACION] = mensaje
        response_dictionary[KEY_RESULTADO_OPERACION] = True

    else:
        if mensaje:
            response_dictionary[KEY_DETALLE_OPERACION] = mensaje
        else:
            response_dictionary[KEY_DETALLE_OPERACION] = DETALLE_OPERACION_VACIA
        response_dictionary[KEY_RESULTADO_OPERACION] = True

    try:
        return dumps(response_dictionary, cls=DjangoJSONEncoder)
    except (KeyError, TypeError, ValueError, SystemError, RuntimeError):
        response_error_dictionary = {KEY_RESULTADO_OPERACION: False}
        response_dictionary[KEY_DETALLE_OPERACION] = DETALLE_ERROR_SISTEMA
        return dumps(response_error_dictionary, cls=DjangoJSONEncoder)


def armar_response_simple(objeto):
    return dumps(objeto, cls=DjangoJSONEncoder)


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
