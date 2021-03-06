# -*- coding: UTF-8 -*-
from django.http import HttpResponse,JsonResponse
from django.db import IntegrityError,transaction
from .supportClases.security_decorators import *

from ..models import *
from supportClases.views_util_functions import *
from supportClases.dto_configuracion_finca import *


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
@manejar_errores()
def mostrarMecanismosRiegoFinca(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if KEY_ID_FINCA in datos:
            if datos[KEY_ID_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            finca_actual = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
            estado_mecanismo_habilitado = EstadoMecanismoRiegoFinca.objects.get(nombreEstadoMecanismoRiegoFinca=
                                                                                ESTADO_HABILITADO)
            mecanismo_riego_finca_list = MecanismoRiegoFinca.objects.filter(finca=finca_actual)
            dto_mecanismo_riego_finca_list = []
            for mecanismo in mecanismo_riego_finca_list:
                ultimo_historico = mecanismo.historicoMecanismoRiegoFincaList.get(
                    fechaFinEstadoMecanismoRiegoFinca__isnull=True)
                dto_mecanismo_riego_finca = DtoMecanismoRiegoFinca(direccionIP=mecanismo.direccionIP,
                                                                   idMecanismoRiegoFinca=mecanismo.idMecanismoRiegoFinca,
                                                                   tipoMecanismoRiego=mecanismo.tipoMecanismoRiego.nombreMecanismo,
                                                                   fechaInstalacion=mecanismo.fechaInstalacion,
                                                                   habilitado=ultimo_historico.estado_mecanismo_riego_finca.nombreEstadoMecanismoRiegoFinca,
                                                                   caudalMaximo=mecanismo.tipoMecanismoRiego.caudalEstandar,
                                                                   presionMaxima=mecanismo.tipoMecanismoRiego.presionEstandar)
                dto_mecanismo_riego_finca_list.append(dto_mecanismo_riego_finca)
            response.content = armar_response_list_content(dto_mecanismo_riego_finca_list)
            response.status_code = 200
            return response
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])
    except (IntegrityError,ValueError) as err:
        print err.args
        response.status_code=401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
@manejar_errores()
def mostrar_mecanismos_nuevos(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if KEY_ID_FINCA in datos:
            if datos[KEY_ID_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            finca_actual = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
            mecanismo_riego_finca_list = MecanismoRiegoFinca.objects.filter(finca=finca_actual)
            tipo_mecanismo_existente_list=[]
            for mecanismo_riego in mecanismo_riego_finca_list:
                tipo_mecanismo_existente_list.append(mecanismo_riego.tipoMecanismoRiego)
            tipo_mecanismo_riego_list = TipoMecanismoRiego.objects.filter(habilitado=True)
            tipo_mecanismo_riego_nuevo_list = []
            for tipo_mecanismo in tipo_mecanismo_riego_list:
                if tipo_mecanismo_existente_list.__contains__(tipo_mecanismo)==False:
                    tipo_mecanismo_riego_nuevo_list.append(tipo_mecanismo)
            response.content = armar_response_list_content(tipo_mecanismo_riego_nuevo_list)
            response.status_code=200
            return response
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])
    except (IntegrityError, TypeError, KeyError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
@manejar_errores()
@permisos_rol_requeridos([PERMISO_PUEDEGESTIONARFINCA, PERMISO_PUEDEASIGNARMECRIEGOAFINCA])
def habilitar_mecanismo_riego_finca(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if KEY_ID_MECANISMO_RIEGO_FINCA in datos:
            if datos[KEY_ID_MECANISMO_RIEGO_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if MecanismoRiegoFinca.objects.filter(
                idMecanismoRiegoFinca=datos[KEY_ID_MECANISMO_RIEGO_FINCA]).__len__() == 0:
                raise ValueError(ERROR_MECANISMO_RIEGO_FINCA_NO_EXISTE, "No existe un mecanismo riego finca con ese id")
            mecanismo_riego_finca = MecanismoRiegoFinca.objects.get(
                idMecanismoRiegoFinca=datos[KEY_ID_MECANISMO_RIEGO_FINCA])
            ultimo_historico = mecanismo_riego_finca.historicoMecanismoRiegoFincaList.get(
                fechaFinEstadoMecanismoRiegoFinca__isnull=True)
            ultimo_historico.fechaFinEstadoMecanismoRiegoFinca = datetime.now(pytz.utc)
            ultimo_historico.save()
            estado_mecanismo_finca_habilitado = EstadoMecanismoRiegoFinca.objects.get(
                nombreEstadoMecanismoRiegoFinca=ESTADO_HABILITADO)
            nuevo_historico = HistoricoMecanismoRiegoFinca(mecanismo_riego_finca=mecanismo_riego_finca,
                                                           estado_mecanismo_riego_finca=
                                                           estado_mecanismo_finca_habilitado,
                                                           fechaInicioEstadoMecanismoRiegoFinca=datetime.now(pytz.utc))
            nuevo_historico.save()
            mecanismo_riego_finca.save()
            response.content = armar_response_content(None)
            response.status_code = 200
            return response
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])
    except (IntegrityError, TypeError, KeyError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_PUT])
@manejar_errores()
@permisos_rol_requeridos([PERMISO_PUEDEGESTIONARFINCA, PERMISO_PUEDEASIGNARMECRIEGOAFINCA])
def agregar_mecanismo_riego_finca(request):
    response=HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_NOMBRE_TIPO_MECANISMO in datos) and (KEY_ID_FINCA in datos) and (KEY_DIRECCION_IP in datos):
            if datos[KEY_NOMBRE_TIPO_MECANISMO] == '' or datos[KEY_ID_FINCA] == '' or datos[KEY_DIRECCION_IP] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            tipo_mecanismo = TipoMecanismoRiego.objects.get(nombreMecanismo=datos[KEY_NOMBRE_TIPO_MECANISMO])
            estado_habilitado = EstadoMecanismoRiegoFinca.objects.get(nombreEstadoMecanismoRiegoFinca=ESTADO_HABILITADO)
            historico_nuevo = HistoricoMecanismoRiegoFinca(fechaInicioEstadoMecanismoRiegoFinca=datetime.now(pytz.utc),
                                                         estado_mecanismo_riego_finca=estado_habilitado)
            finca_actual = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
            if MecanismoRiegoFinca.objects.filter(finca=finca_actual, tipoMecanismoRiego=tipo_mecanismo).__len__() != 0:
                raise ValueError (ERROR_MECANISMO_RIEGO_FINCA_YA_EXISTE,
                                  "La finca ya dispone de este mecanismo, en caso de "
                                  "que no este habilitado elija la opcion habilitar")
            if MecanismoRiegoFinca.objects.filter(direccionIP=datos[KEY_DIRECCION_IP],finca=finca_actual,
                                                  tipoMecanismoRiego=tipo_mecanismo).__len__() != 0:
                raise ValueError(ERROR_IP_YA_USADA, "Ya existe un mecanismo con esa IP")

            mecanismo_riego_finca = MecanismoRiegoFinca(finca=finca_actual, tipoMecanismoRiego=tipo_mecanismo,
                                                      fechaInstalacion=datetime.now(pytz.utc),
                                                        direccionIP=datos[KEY_DIRECCION_IP])
            mecanismo_riego_finca.save()
            historico_nuevo.mecanismo_riego_finca = mecanismo_riego_finca
            mecanismo_riego_finca.historicoMecanismoRiegoFincaList.add(historico_nuevo, bulk=False)
            historico_nuevo.save()
            mecanismo_riego_finca.save()
            response.content = armar_response_content(None)
            response.status_code = 200
            return response
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])
    except (IntegrityError, TypeError, KeyError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
@manejar_errores()
@permisos_rol_requeridos([PERMISO_PUEDEGESTIONARFINCA, PERMISO_PUEDEASIGNARMECRIEGOAFINCA])
def deshabilitar_mecanismo_riego_finca(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if KEY_ID_MECANISMO_RIEGO_FINCA in datos:
            if datos[KEY_ID_MECANISMO_RIEGO_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if MecanismoRiegoFinca.objects.filter(
                idMecanismoRiegoFinca=datos[KEY_ID_MECANISMO_RIEGO_FINCA]).__len__() == 0:
                raise ValueError(ERROR_MECANISMO_RIEGO_FINCA_NO_EXISTE, "No existe un mecanismo riego finca con ese id")
            mecanismo_riego_finca = MecanismoRiegoFinca.objects.get(idMecanismoRiegoFinca=
                                                                    datos[KEY_ID_MECANISMO_RIEGO_FINCA])
            ultimo_historico_mecanismo_finca = HistoricoMecanismoRiegoFinca.objects.get(
                mecanismo_riego_finca=mecanismo_riego_finca, fechaFinEstadoMecanismoRiegoFinca__isnull=True )
            if ultimo_historico_mecanismo_finca.estado_mecanismo_riego_finca.nombreEstadoMecanismoRiegoFinca == \
                    ESTADO_DESHABILITADO:
                raise ValueError(ERROR_MECANISMO_RIEGO_FINCA_NO_HABILITADO,
                                 "El mecanismo de la finca seleccionado ya se encuentra deshabilitado")
            lista_mecanismo_riego_sector = mecanismo_riego_finca.mecanismoRiegoSectorList.all()
            estado_mecanismo_sector_habilitado = EstadoMecanismoRiegoFincaSector.objects.get(
                nombreEstadoMecanismoRiegoFincaSector=ESTADO_HABILITADO)
            estado_riego_en_ejecucion = EstadoEjecucionRiego(nombreEstadoEjecucionRiego=ESTADO_EN_EJECUCION)
            for mecanismo_riego_sector in lista_mecanismo_riego_sector:
                if mecanismo_riego_sector.historicoMecanismoRiegoFincaSector.filter(
                        estado_mecanismo_riego_finca_sector=estado_mecanismo_sector_habilitado,
                        fechaFinEstadoMecanismoRiegoFincaSector__isnull=True).__len__() == 1:
                    if mecanismo_riego_sector.ejecucionRiegoList.all().__len__() != 0:
                        for ejecucion_riego in mecanismo_riego_sector.ejecucionRiegoList.all():
                            if ejecucion_riego.estado_ejecucion_riego == estado_riego_en_ejecucion:
                                raise ValueError(ERROR_RIEGO_EN_EJECUCION, "Actualmente el mecanismo esta regando en "
                                                                           "el sector " +
                                                                            mecanismo_riego_sector.sector.numeroSector
                                                                            + ", detenga el riego para poder eliminar "
                                                                              "el mecanismo"
                                                )


            ultimo_historico_mecanismo_finca.fechaFinEstadoMecanismoRiegoFinca = datetime.now(pytz.utc)
            ultimo_historico_mecanismo_finca.save()
            estado_mecanismo_finca_deshabilitado = EstadoMecanismoRiegoFinca.objects.get(nombreEstadoMecanismoRiegoFinca=
                                                                                         ESTADO_DESHABILITADO)
            nuevo_historico_mecanismo_finca = HistoricoMecanismoRiegoFinca(estado_mecanismo_riego_finca=
                                                                           estado_mecanismo_finca_deshabilitado,
                                                                           fechaInicioEstadoMecanismoRiegoFinca=
                                                                           datetime.now(pytz.utc),
                                                                           mecanismo_riego_finca=mecanismo_riego_finca)
            nuevo_historico_mecanismo_finca.save()
            mecanismo_riego_finca.save()
            estado_mecanismo_sector_deshabilitado = EstadoMecanismoRiegoFincaSector.objects.get(
                nombreEstadoMecanismoRiegoFincaSector=ESTADO_DESHABILITADO)
            estado_configuracion_riego_habilitada = EstadoConfiguracionRiego.objects.get(
                nombreEstadoConfiguracionRiego=ESTADO_HABILITADO)
            estado_configuracion_riego_deshabilitada = EstadoConfiguracionRiego.objects.get(
                nombreEstadoConfiguracionRiego=ESTADO_DESHABILITADO)

            mecanismo_riego_sector_lista = mecanismo_riego_finca.mecanismoRiegoSectorList.all()
            for mecanismo_sector in mecanismo_riego_sector_lista:
                if HistoricoMecanismoRiegoFincaSector.objects.filter(estado_mecanismo_riego_finca_sector=
                                                                     estado_mecanismo_sector_habilitado,
                                                                     fechaFinEstadoMecanismoRiegoFincaSector__isnull=
                                                                     True).__len__() == 1:
                    lista_configuraciones_riego = mecanismo_sector.configuracionriego_set.all()
                    for configuracion in lista_configuraciones_riego:
                        if configuracion.historicoEstadoConfiguracionRiegoList.filter(
                                estado_configuracion_riego=estado_configuracion_riego_habilitada,
                                fechaFinEstadoConfiguracionRiego__isnull=True).__len__() == 1:
                            ultimo_historico_configuracion_riego = configuracion.historicoEstadoConfiguracionRiegoList.\
                                get(estado_configuracion_riego=estado_configuracion_riego_habilitada,
                                    fechaFinEstadoConfiguracionRiego__isnull=True)
                            ultimo_historico_configuracion_riego.fechaFinEstadoConfiguracionRiego = \
                                datetime.now(pytz.utc)
                            ultimo_historico_configuracion_riego.save()
                            nuevo_historico_configuracion_riego = HistoricoEstadoConfiguracionRiego(
                                configuracion_riego=configuracion,
                                fechaInicioEstadoConfiguracionRiego=datetime.now(pytz.utc),
                                estado_configuracion_riego=estado_configuracion_riego_deshabilitada)
                            nuevo_historico_configuracion_riego.save()
                    ultimo_historico_mecanismo_sector = HistoricoMecanismoRiegoFincaSector.objects.get(
                        estado_mecanismo_riego_finca_sector=estado_mecanismo_sector_habilitado,
                        fechaFinEstadoMecanismoRiegoFincaSector__isnull=True)
                    ultimo_historico_mecanismo_sector.fechaFinEstadoMecanismoRiegoFincaSector = datetime.now(pytz.utc)
                    ultimo_historico_mecanismo_sector.save()
                    nuevo_historico_mecanismo_sector = HistoricoMecanismoRiegoFincaSector(
                        estado_mecanismo_riego_finca_sector=estado_mecanismo_sector_deshabilitado,
                        fechaInicioEstadoMecanismoRiegoFincaSector=datetime.now(pytz.utc),
                        mecanismo_riego_finca_sector=mecanismo_sector)
                    nuevo_historico_mecanismo_sector.save()
            mecanismo_riego_finca.save()
            response.content = armar_response_content(None)
            response.status_code = 200
            return response
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])
    except (IntegrityError, TypeError, KeyError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")