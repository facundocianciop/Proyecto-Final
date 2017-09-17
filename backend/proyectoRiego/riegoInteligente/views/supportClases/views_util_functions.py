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


def armar_response_content(objeto):
    response_dictionary = {}

    if objeto is not None:
        try:
            response_dictionary = objeto.as_json()
        except (TypeError, ValueError):
            pass

    response_dictionary[KEY_RESULTADO_OPERACION] = True

    try:
        return dumps(response_dictionary, cls=DjangoJSONEncoder)
    except (TypeError, ValueError):
        response_error_dictionary = {KEY_RESULTADO_OPERACION: False}
        return dumps(response_error_dictionary, cls=DjangoJSONEncoder)


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
