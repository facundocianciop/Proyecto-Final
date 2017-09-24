# -*- coding: UTF-8 -*-

from django.contrib.auth.models import User
from django.db import IntegrityError

from ..models import Finca
from supportClases.dto_modulo_finca import *
from supportClases.security_util_functions import *  # Se importa para que se ejecuten los handlers de sesion
from supportClases.security_decorators import *
from supportClases.views_util_functions import *
from supportClases.views_constants import *
from supportClases.error_handler import *


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def iniciar_riego_manualente (request):
    response = HttpResponse()
    try:
        user = request.user
        usuario = user.datosusuario



        response.content = armar_response_content(None)
        response.status_code = 200

        return response

    except ValueError as err:
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, TypeError, KeyError):
        return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, "Datos incorrectos")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def detener_riego_manualente(request):
    response = HttpResponse()
    try:
        user = request.user
        usuario = user.datosusuario



        response.content = armar_response_content(None)
        response.status_code = 200

        return response

    except ValueError as err:
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, TypeError, KeyError):
        return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, "Datos incorrectos")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def obtener_riegos_en_ejecucion(request):
    response = HttpResponse()
    try:
        user = request.user
        usuario = user.datosusuario



        response.content = armar_response_content(None)
        response.status_code = 200

        return response

    except ValueError as err:
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, TypeError, KeyError):
        return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, "Datos incorrectos")
