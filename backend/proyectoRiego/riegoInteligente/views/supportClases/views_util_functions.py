import string
import random
from json import loads, dumps

from django.core.serializers.json import DjangoJSONEncoder

from views_constants import *


def obtener_datos_json(request):
    try:
        received_json_data = str(request.body)
        datos = loads(received_json_data)
        return datos
    except (TypeError, ValueError):
        return ""


def armar_response_list_content(lista):
    response_dictionary = [item.as_json() for item in lista]
    return dumps(response_dictionary, cls=DjangoJSONEncoder)


def armar_response_content(objeto, *mensaje):
    response_dictionary = {}

    if objeto is not None:
        try:
            response_dictionary = objeto.as_json()
        except (TypeError, ValueError):
            pass

        if mensaje:
            response_dictionary[KEY_DETALLE_OPERACION] = mensaje
        response_dictionary[KEY_RESULTADO_OPERACION] = True

    else:
        if mensaje:
            response_dictionary[KEY_DETALLE_OPERACION] = mensaje
        else:
            response_dictionary[KEY_DETALLE_OPERACION] = "No hay datos"
        response_dictionary[KEY_RESULTADO_OPERACION] = True

    try:
        return dumps(response_dictionary, cls=DjangoJSONEncoder)
    except (TypeError, ValueError):
        response_error_dictionary = {KEY_RESULTADO_OPERACION: False}
        return dumps(response_error_dictionary, cls=DjangoJSONEncoder)


def armar_response_simple(objeto):
    return dumps(objeto, cls=DjangoJSONEncoder)


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
