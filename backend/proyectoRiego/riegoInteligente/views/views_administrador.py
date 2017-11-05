# -*- coding: UTF-8 -*-

from django.template import loader

from supportClases.security_util_functions import *  # Se importa para que se ejecuten los handlers de sesion
from supportClases.security_decorators import *
from supportClases.views_constants import *
from supportClases.error_handler import *

from ..models import *


@transaction.atomic()
def fincas_por_aprobar(request):
    response = HttpResponse()
    if not request.user.is_staff:
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


# noinspection PyPep8Naming
@transaction.atomic()
def aprobar_finca(request, idFinca):

    response = HttpResponse()
    admin = request.POST.get("administrador",)

    if User.objects.filter(username=admin).__len__() == 0:
        raise ValueError(ERROR_USUARIO_NO_ADMINISTRADOR, "No tiene permisos para acceder a este sitio")
    user = User.objects.get(username=admin)

    if not user.is_staff:
        raise ValueError(ERROR_NO_TIENE_PERMISOS, "El usuario no tiene permisos para acceder a esta pagina")
    try:
            if Finca.objects.filter(idFinca=idFinca).__len__() == 1:
                    finca_por_aprobar = Finca.objects.get(idFinca=idFinca)
                    ultimo_historico = finca_por_aprobar.historicoEstadoFincaList.get(fechaFinEstadoFinca__isnull=True)
                    if ultimo_historico.estadoFinca.nombreEstadoFinca == ESTADO_HABILITADO:
                        raise ValueError(ERROR_FINCA_YA_APROBADA, "Esta finca ya esta aprobada")

                    estado_habilitado = EstadoFinca.objects.get(nombreEstadoFinca=ESTADO_HABILITADO)
                    estado_pendiente_aprobacion = EstadoFinca.objects.get(nombreEstadoFinca=ESTADO_PENDIENTE_APROBACION)
                    historico_viejo = HistoricoEstadoFinca.objects.get(estadoFinca=estado_pendiente_aprobacion,
                                                                       finca=finca_por_aprobar)
                    historico_viejo.fechaFinEstadoFinca = datetime.now(pytz.utc)
                    historico_viejo.save()
                    historico_nuevo = HistoricoEstadoFinca(estadoFinca=estado_habilitado, finca=finca_por_aprobar,
                                                           fechaInicioEstadoFinca=datetime.now(pytz.utc))
                    finca_por_aprobar.historicoEstadoFincaList.add(historico_nuevo, bulk=False)
                    finca_por_aprobar.save()
                    usuario_finca = UsuarioFinca.objects.get(finca=finca_por_aprobar)
                    rol_encargado = Rol.objects.get(nombreRol=ROL_ENCARGADO)
                    rol_usuario_finca = RolUsuarioFinca()
                    rol_usuario_finca.fechaAltaRolUsuarioFinca = datetime.now(pytz.utc)
                    rol_usuario_finca.rol = rol_encargado
                    rol_usuario_finca.save()
                    usuario_finca.rolUsuarioFincaList.add(rol_usuario_finca)

                    template = loader.get_template('admin/riegoInteligente/fincaAprobada.html')
                    context = {
                        'finca': finca_por_aprobar,
                        'user': request.user,
                    }

                    return HttpResponse(template.render(context, request))

            else:
                raise ValueError(ERROR_FINCA_NO_ENCONTRADA, "No se encontro la finca seleccionada")

    except ValueError as err:
        return build_bad_request_error(response, err.args[0], err.args[1])
    except (IntegrityError, TypeError, KeyError)as err:
        print err.args
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


# noinspection PyPep8Naming
@transaction.atomic()
def no_aprobar_finca(request, idFinca):

    response = HttpResponse()
    admin = request.POST.get("administrador", )

    if User.objects.filter(username=admin).__len__() == 0:
        raise ValueError(ERROR_USUARIO_NO_ADMINISTRADOR, "No tiene permisos para acceder a este sitio")
    user = User.objects.get(username=admin)

    if not user.is_staff:
        raise ValueError(ERROR_NO_TIENE_PERMISOS, "El usuario no tiene permisos para acceder a esta pagina")
    try:
            if Finca.objects.filter(idFinca=idFinca).__len__() == 1:
                    finca_por_aprobar = Finca.objects.get(idFinca=idFinca)
                    ultimo_historico = finca_por_aprobar.historicoEstadoFincaList.get(fechaFinEstadoFinca__isnull=True)
                    if ultimo_historico.estadoFinca.nombreEstadoFinca == ESTADO_NO_APROBADO:
                        raise ValueError(ERROR_FINCA_YA_DESAPROBADA, "Esta finca ya esta desaprobada")
                    estado_pendiente_aprobacion = EstadoFinca.objects.get(nombreEstadoFinca=ESTADO_PENDIENTE_APROBACION)
                    estado_no_aprobada = EstadoFinca.objects.get(nombreEstadoFinca=ESTADO_NO_APROBADO)
                    historico_viejo = HistoricoEstadoFinca.objects.get(estadoFinca=estado_pendiente_aprobacion,
                                                                       finca=finca_por_aprobar)
                    historico_viejo.fechaFinEstadoFinca = datetime.now(pytz.utc)
                    historico_viejo.save()
                    historico_nuevo = HistoricoEstadoFinca(estadoFinca=estado_no_aprobada, finca=finca_por_aprobar,
                                                           fechaInicioEstadoFinca=datetime.now(pytz.utc))
                    historico_nuevo.save()
                    finca_por_aprobar.save()

                    template = loader.get_template('admin/riegoInteligente/fincaNoAprobada.html')
                    context = {
                        'finca': finca_por_aprobar,
                        'user': request.user,
                    }
                    return HttpResponse(template.render(context, request))

            else:
                raise ValueError(ERROR_FINCA_NO_ENCONTRADA, "No se encontro la finca seleccionada")

    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])
    except (IntegrityError, TypeError, KeyError):
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")
