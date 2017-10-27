# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User
from django.db import IntegrityError
from supportClases.dto_modulo_finca import *
from supportClases.security_util_functions import *  # Se importa para que se ejecuten los handlers de sesion
from supportClases.security_decorators import *
from supportClases.views_util_functions import *
from supportClases.views_constants import *
from supportClases.error_handler import *
from django.http import HttpResponse
from django.template import loader
from .forms import NameForm
from ..models import *


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_GET])
def fincas_por_aprobar(request):
    response = HttpResponse()
    if request.user.is_staff == False:
        raise ValueError(ERROR_NO_TIENE_PERMISOS, "El usuario no tiene permisos para acceder a esta pagina")
    try:
        estado_pendiente = EstadoFinca.objects.get(nombreEstadoFinca=ESTADO_PENDIENTE_APROBACION)
        historicos_pendientes = HistoricoEstadoFinca.objects.filter(estadoFinca=estado_pendiente,
                                                                    fechaFinEstadoFinca__isnull=True)
        fincas_pendientes = []
        for historico in historicos_pendientes:
                fincas_pendientes.append(historico.finca)
        template = loader.get_template('admin/riegoInteligente/fincasPorAprobar.html')
        context = {
            'fincas': fincas_pendientes,
            'user': request.user,
        }
        return HttpResponse(template.render(context, request))

    except (IntegrityError, TypeError, KeyError):
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")

