    # -*- coding: UTF-8 -*-
from django.db import IntegrityError, transaction
from .supportClases.security_decorators import *
from ..models import *
from supportClases.views_util_functions import *
from supportClases.error_handler import *
from supportClases.dto_modulo_configuracion_sectores import *


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_PUT])
def crear_sector(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        finca_actual = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
        estado_habilitado = EstadoSector.objects.get(nombreEstadoSector=ESTADO_HABILITADO)

        if Sector.objects.filter(numeroSector=datos[KEY_NUMERO_SECTOR], finca=finca_actual).__len__() == 1:
            sector = Sector.objects.get(numeroSector=datos[KEY_NUMERO_SECTOR], finca=finca_actual)
            if sector.historicoEstadoSectorList.filter(fechaFinEstadoSector__isnull=True,
                                                       estado_sector=estado_habilitado).__len__() == 1:
                raise ValueError(ERROR_SECTOR_YA_EXISTENTE,"Ya existe un sector con ese numero")
        if Sector.objects.filter(nombreSector=datos[KEY_NOMBRE_SECTOR], finca=finca_actual).__len__() == 1:
            sector = Sector.objects.get(numeroSector=datos[KEY_NOMBRE_SECTOR], finca=finca_actual)
            if sector.historicoEstadoSectorList.filter(fechaFinEstadoSector__isnull=True,
                                                       estado_sector=estado_habilitado).__len__() ==1:
                raise ValueError(ERROR_SECTOR_YA_EXISTENTE, "Ya existe un sector con ese nombre")
        sector_nuevo = Sector(numeroSector=datos[KEY_NUMERO_SECTOR], nombreSector=datos[KEY_NOMBRE_SECTOR],
                              descripcionSector=datos[KEY_DESCRIPCION_SECTOR], superficie=datos[KEY_SUPERFICIE_SECTOR],
                              finca=finca_actual
                              )
        sector_nuevo.save()
        historico_nuevo = HistoricoEstadoSector(estado_sector=estado_habilitado, sector=sector_nuevo,
                                                fechaInicioEstadoSector=datetime.now())
        historico_nuevo.save()
        finca_actual.save()
        response.content = armar_response_content(None)
        response.status_code = 200
        return response
    except ValueError as err:
        return build_bad_request_error(response, err.args[0], err.args[1])
    except (IntegrityError, TypeError, KeyError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def modificar_sector(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:

        sector_seleccionado = Sector.objects.get(idSector=datos[KEY_ID_SECTOR])
        estado_habilitado = EstadoSector.objects.get(nombreEstadoSector=ESTADO_HABILITADO)
        if HistoricoEstadoSector.objects.filter(sector=sector_seleccionado, estado_sector=estado_habilitado,
                                                             fechaFinEstadoSector__isnull=True).__len__() != 1:
            raise ValueError(ERROR_SECTOR_NO_HABILITADO, "El sector seleccionado no esta habilitado")

        sector_seleccionado.nombreSector = datos[KEY_NOMBRE_SECTOR]
        sector_seleccionado.descripcionSector = datos[KEY_DESCRIPCION_SECTOR]
        sector_seleccionado.superficie = datos[KEY_SUPERFICIE_SECTOR]
        sector_seleccionado.save()
        response.content = armar_response_content(None)
        response.status_code = 200
        return response
    except ValueError as err:
        return build_bad_request_error(response,err.args[0], err.args[1])
    except (IntegrityError, TypeError, KeyError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def eliminar_sector(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:

        sector_seleccionado = Sector.objects.get(idSector=datos[KEY_ID_SECTOR])
        estado_habilitado = EstadoSector.objects.get(nombreEstadoSector=ESTADO_HABILITADO)
        if HistoricoEstadoSector.objects.filter(sector=sector_seleccionado, estado_sector=estado_habilitado,
                                                             fechaFinEstadoSector__isnull=True).__len__() != 1:
            raise ValueError(ERROR_SECTOR_NO_HABILITADO, "El sector seleccionado no esta habilitado")
        historico_viejo = HistoricoEstadoSector.objects.get(sector=sector_seleccionado, estado_sector=estado_habilitado,
                                                            fechaFinEstadoSector__isnull=True)
        historico_viejo.fechaFinEstadoSector = datetime.now()
        historico_viejo.save()
        estado_deshabilitado = EstadoSector.objects.get(nombreEstadoSector=ESTADO_DESHABILITADO)
        historico_nuevo = HistoricoEstadoSector(fechaInicioEstadoSector=datetime.now(),
                                                estado_sector=estado_deshabilitado)
        sector_seleccionado.historicoEstadoSectorList.add(historico_nuevo, bulk=False)
        sector_seleccionado.save()
        mecanismo_riego_sector_lista = MecanismoRiegoFincaSector.objects.filter(sector=sector_seleccionado)
        estado_mecanismo_riego_sector_habilitado = EstadoMecanismoRiegoFincaSector.objects.get(
            nombreEstadoMecanismoRiegoFincaSector=ESTADO_HABILITADO)
        for mecanismo_riego_sector in mecanismo_riego_sector_lista:
            if mecanismo_riego_sector.historicoMecanismoRiegoFincaSector.filter(
                    fechaFinEstadoMecanismoRiegoFincaSector__isnull=True, estado_mecanismo_riego_finca_sector=
                    estado_mecanismo_riego_sector_habilitado).__len__() == 1:
                mecanismo_riego_sector_deshabilitar = mecanismo_riego_sector
                ultimo_historico_mecanismo_riego_sector = mecanismo_riego_sector.historicoMecanismoRiegoFincaSector.get(
                    fechaFinEstadoMecanismoRiegoFincaSector__isnull=True, estado_mecanismo_riego_finca_sector=
                estado_mecanismo_riego_sector_habilitado)
                ultimo_historico_mecanismo_riego_sector.fechaFinEstadoMecanismoRiegoFincaSector = datetime.now()
                ultimo_historico_mecanismo_riego_sector.save()
                estado_mecanismo_riego_sector_deshabilitado = EstadoMecanismoRiegoFincaSector.objects.get(
                    nombreEstadoMecanismoRiegoFincaSector=ESTADO_DESHABILITADO)
                nuevo_historico_mecanismo_riego_sector = HistoricoMecanismoRiegoFincaSector(
                    mecanismo_riego_finca_sector=mecanismo_riego_sector_deshabilitar,
                    fechaInicioEstadoMecanismoRiegoFincaSector= datetime.now(),
                    estado_mecanismo_riego_finca_sector=estado_mecanismo_riego_sector_deshabilitado)
                nuevo_historico_mecanismo_riego_sector.save()

                response.content = armar_response_content(None)
                response.status_code = 200
                return response
    except ValueError as err:
        return build_bad_request_error(response,err.args[0], err.args[1])
    except (IntegrityError, TypeError, KeyError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def mostrar_sectores(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        finca_actual = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
        estado_habilitado = EstadoSector.objects.get(nombreEstadoSector=ESTADO_HABILITADO)
        lista_sectores = Sector.objects.filter(finca=finca_actual)
        sectores_habilitados = []
        for sector in lista_sectores:
            if HistoricoEstadoSector.objects.filter(sector=sector, fechaFinEstadoSector__isnull=True,
                                                                 estado_sector=estado_habilitado).__len__() ==1:
                sectores_habilitados.append(sector)

        response.content = armar_response_list_content(sectores_habilitados)
        response.status_code = 200
        return response
    except ValueError as err:
        return build_bad_request_error(response,err.args[0], err.args[1])
    except (IntegrityError, TypeError, KeyError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def mostrar_mecanismo_riego_sector(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        estado_habilitado = EstadoSector.objects.get(nombreEstadoSector=ESTADO_HABILITADO)
        sector_seleccionado = Sector.objects.get(idSector=datos[KEY_ID_SECTOR])
        if HistoricoEstadoSector.objects.filter(sector=sector_seleccionado, estado_sector=estado_habilitado,
                                                fechaFinEstadoSector__isnull=True).__len__() != 1:
            raise ValueError(ERROR_SECTOR_NO_HABILITADO, "El sector seleccionado no esta habilitado")
        estado_mecanismo_sector_habilitado = EstadoMecanismoRiegoFincaSector.objects.get(nombreEstadoMecanismoRiegoFincaSector=ESTADO_HABILITADO)
        mecanismo_sector_lista = sector_seleccionado.mecanismoRiegoFincaSector.all()
        for mecanismo in mecanismo_sector_lista:
            if mecanismo.historicoMecanismoRiegoFincaSector.filter(
                    estado_mecanismo_riego_finca_sector= estado_mecanismo_sector_habilitado,
                    fechaFinEstadoMecanismoRiegoFincaSector__isnull=True).__len__() == 1:
                response.content = armar_response_content(mecanismo)
                response.status_code = 200
                return response
        response.content = "[]"
        response.status_code = 200
        return response
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
def asignar_mecanismo_a_sector(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        sector_seleccionado = Sector.objects.get(idSector=datos[KEY_ID_SECTOR])
        mecanismo_riego_sector_lista = sector_seleccionado.mecanismoRiegoFincaSector.all()
        estado_mecanismo_riego_finca_sector_habilitado = EstadoMecanismoRiegoFincaSector.objects.get(
            nombreEstadoMecanismoRiegoFincaSector=ESTADO_HABILITADO)
        for mecanismo_sector in mecanismo_riego_sector_lista:
            if HistoricoMecanismoRiegoFincaSector.objects.filter(fechaFinEstadoMecanismoRiegoFincaSector__isnull=True,
                                                                 mecanismo_riego_finca_sector=mecanismo_sector,
                                                                 estado_mecanismo_riego_finca_sector=
                                                                 estado_mecanismo_riego_finca_sector_habilitado).__len__() != 0:
                raise ValueError (ERROR_SECTOR_YA_TIENE_MECANISMO_HABILITADO,
                                  "El sector ya tiene un mecanismo de riego asignado")
        mecanismo_riego_finca_seleccionado = MecanismoRiegoFinca.objects.get(idMecanismoRiegoFinca=
                                                                             datos[KEY_ID_MECANISMO_RIEGO_FINCA])
        historico_mecanismo_riego_finca_actual = mecanismo_riego_finca_seleccionado.historicoMecanismoRiegoFincaList.\
            get(fechaFinEstadoMecanismoRiegoFinca__isnull=True)
        if historico_mecanismo_riego_finca_actual.estado_mecanismo_riego_finca.nombreEstadoMecanismoRiegoFinca \
                != ESTADO_HABILITADO:
            raise ValueError(ERROR_MECANISMO_RIEGO_FINCA_NO_HABILITADO,
                             "El mecanismo seleccionado no se encuentra habilitado para la finca")
        historico_sector_seleccionado_actual = sector_seleccionado.historicoEstadoSectorList.get(
            fechaFinEstadoSector__isnull=True)
        if historico_sector_seleccionado_actual.estado_sector.nombreEstadoSector != ESTADO_HABILITADO:
            raise ValueError(ERROR_SECTOR_NO_HABILITADO, "El sector seleccionado no se encuentra habilitado")
        mecanismo_riego_sector = MecanismoRiegoFincaSector(mecanismo_riego_finca=mecanismo_riego_finca_seleccionado,
                                                           sector=sector_seleccionado)
        if KEY_MECANISMO_RIEGO_CAUDAL in datos:
            mecanismo_riego_sector.caudal = datos[KEY_MECANISMO_RIEGO_CAUDAL]
        else:
            mecanismo_riego_sector.caudal = mecanismo_riego_finca_seleccionado.tipoMecanismoRiego.caudalEstandar
        if KEY_MECANISMO_RIEGO_PRESION in datos:
            mecanismo_riego_sector.presion = datos[KEY_MECANISMO_RIEGO_PRESION]
        else:
            mecanismo_riego_sector.presion = mecanismo_riego_finca_seleccionado.tipoMecanismoRiego.presionEstandar
        mecanismo_riego_sector.save()
        nuevo_historico = HistoricoMecanismoRiegoFincaSector(fechaInicioEstadoMecanismoRiegoFincaSector=datetime.now(),
                                                             estado_mecanismo_riego_finca_sector
                                                             =estado_mecanismo_riego_finca_sector_habilitado)
        mecanismo_riego_sector.historicoMecanismoRiegoFincaSector.add(nuevo_historico, bulk=False)
        mecanismo_riego_sector.save()
        response.content = armar_response_content(None)
        response.status_code = 200
        return response
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
def deshabilitar_mecanismo_riego_sector(request):
    response=HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if MecanismoRiegoFincaSector.objects.filter(
            idMecanismoRiegoFincaSector=datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR]).__len__() == 0:
            raise ValueError(ERROR_MECANISMO_RIEGO_FINCA_SECTOR_NO_EXISTE, "El idMecanismoRiegoFincaSector no existe")
        mecanismo_riego_finca_sector = MecanismoRiegoFincaSector.objects.get(
            idMecanismoRiegoFincaSector=datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR])
        estado_mecanismo_sector_habilitado = EstadoMecanismoRiegoFincaSector(
            nombreEstadoMecanismoRiegoFincaSector=ESTADO_HABILITADO)
        if HistoricoMecanismoRiegoFincaSector.objects.filter(
            mecanismo_riego_finca_sector=mecanismo_riego_finca_sector, fechaFinEstadoMecanismoRiegoFincaSector__isnull=True,
            estado_mecanismo_riego_finca_sector=estado_mecanismo_sector_habilitado).__len__() != 1:
            raise ValueError (ERROR_MECANISMO_RIEGO_FINCA_SECTOR_NO_HABILITADO,
                              "El mecanismo sector no se encuentra habilitado")

        ultimo_historico_mecanismo_finca_sector = HistoricoMecanismoRiegoFincaSector.objects.get(
            mecanismo_riego_finca_sector=mecanismo_riego_finca_sector, fechaFinEstadoMecanismoRiegoFinca__isnull=True,
            estado_mecanismo_riego_finca_sector=estado_mecanismo_sector_habilitado)
        ultimo_historico_mecanismo_finca_sector.fechaFinEstadoMecanismoRiegoFinca = datetime.now()
        ultimo_historico_mecanismo_finca_sector.save()
        estado_mecanismo_finca_sector_deshabilitado = EstadoMecanismoRiegoFincaSector.objects.get(
            nombreEstadoMecanismoRiegoFincaSector=ESTADO_DESHABILITADO)
        nuevo_historico_mecanismo_finca_sector = HistoricoMecanismoRiegoFincaSector(
            estado_mecanismo_riego_finca_sector=estado_mecanismo_finca_sector_deshabilitado,
            fechaInicioEstadoMecanismoRiegoFincaSector=datetime.now(),
            mecanismo_riego_finca_sector=mecanismo_riego_finca_sector)
        nuevo_historico_mecanismo_finca_sector.save()
        mecanismo_riego_finca_sector.save()
        response.content = armar_response_content(None)
        response.status_code = 200
        return response
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])
    except (IntegrityError, TypeError, KeyError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_GET])
def mostrar_subtipos_tipos_cultivos(request):
    response = HttpResponse()
    try:
        subtipos_lista = SubtipoCultivo.objects.all()
        dto_tipo_subtipo_lista = []
        for subtipo in subtipos_lista:
            dto_tipo_subtipo = DtoTipoSubtipo(nombreSubtipo=subtipo.nombreSubtipo,
                                              nombreTipo=subtipo.tipo_cultivo.nombreTipoCultivo)
            dto_tipo_subtipo_lista.append(dto_tipo_subtipo)
        response.content = armar_response_list_content(dto_tipo_subtipo_lista)
        response.status_code = 200
        return response
    except (IntegrityError, TypeError, KeyError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_PUT])
def asignar_cultivo_a_sector(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        sector_seleccionado = Sector.objects.get(idSector=datos[KEY_ID_SECTOR])
        if sector_seleccionado.cultivo_set.filter(habilitado=True).__len__() !=0:
            raise ValueError (ERROR_SECTOR_YA_TIENE_CULTIVO_ASIGNADO, "El sector ya tiene un cultivo asignado")
        estado_habilitado = EstadoSector.objects.get(nombreEstadoSector=ESTADO_HABILITADO)
        if HistoricoEstadoSector.objects.filter(sector=sector_seleccionado, estado_sector=estado_habilitado,
                                                fechaFinEstadoSector__isnull=True).__len__() != 1:
            raise ValueError(ERROR_SECTOR_NO_HABILITADO, "El sector seleccionado no esta habilitado")
        if SubtipoCultivo.objects.filter(nombreSubtipo=datos[KEY_NOMBRE_SUBTIPO_CULTIVO]).__len__() != 1:
            raise ValueError(ERROR_SUBTIPO_CULTIVO_NO_EXISTENTE, "El subtipo seleccionado no existe")
        if SubtipoCultivo.objects.filter(nombreSubtipo=datos[KEY_NOMBRE_SUBTIPO_CULTIVO],
                                         habilitado=True).__len__() != 1:
            raise ValueError(ERROR_SUBTIPO_CULTIVO_NO_HABILITADO, "El subtipo seleccionado no esta habilitado")
        subtipo_seleccionado = SubtipoCultivo.objects.get(nombreSubtipo=datos[KEY_NOMBRE_SUBTIPO_CULTIVO])
        if subtipo_seleccionado.tipo_cultivo.habilitado != True:
            raise ValueError(ERROR_TIPO_CULTIVO_NO_HABILITADO, "Este tipo de cultivo no esta habilitado")
        cultivo = Cultivo(nombre=datos[KEY_NOMBRE_CULTIVO], descripcion=datos[KEY_DESCRIPCION_CULTIVO], habilitado=True,
                          sector=sector_seleccionado, fechaPlantacion=datos[KEY_FECHA_PLANTACION],
                          subtipo_cultivo=subtipo_seleccionado)
        cultivo.save()
        response.content = armar_response_content(None)
        response.status_code = 200
        return response
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
def modificar_cultivo_sector(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_ID_CULTIVO & KEY_DESCRIPCION_CULTIVO and KEY_FECHA_PLANTACION & KEY_NOMBRE_CULTIVO)  in datos:
            if datos[KEY_ID_CULTIVO] == '' or datos[KEY_DESCRIPCION_CULTIVO] == '' or datos[KEY_FECHA_PLANTACION] == '' or datos[KEY_NOMBRE_CULTIVO] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if Cultivo.objects.filter(idCultivo=datos[KEY_ID_CULTIVO]).__len__() == 0:
                raise ValueError(ERROR_CULTIVO_NO_EXISTENTE, "El id del cultivo no es correcto")
            if Cultivo.objects.filter(idCultivo=datos[KEY_ID_CULTIVO], habilitado=True).__len__() == 0:
                raise ValueError(ERROR_CULTIVO_NO_HABILITADO, "El cultivo no está habilitado")
            cultivo_seleccionado = Cultivo.objects.get(idCultivo=datos[KEY_ID_CULTIVO])
            if KEY_DESCRIPCION_CULTIVO in datos:
                cultivo_seleccionado.descripcion = datos[KEY_DESCRIPCION_CULTIVO]
            if KEY_FECHA_PLANTACION in datos:
                cultivo_seleccionado.fechaPlantacion = datos[KEY_FECHA_PLANTACION]
            if KEY_NOMBRE_CULTIVO in datos:
                cultivo_seleccionado.nombre = datos[KEY_NOMBRE_CULTIVO]
            cultivo_seleccionado.save()
            response.content = armar_response_content(None)
            response.status_code = 200
            return response
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
def deshabilitar_cultivo_sector(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if KEY_ID_CULTIVO in datos:
            if datos[KEY_ID_CULTIVO] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if Cultivo.objects.filter(idCultivo=datos[KEY_ID_CULTIVO]).__len__() == 0:
                raise ValueError(ERROR_CULTIVO_NO_EXISTENTE, "El id del cultivo no es correcto")
            if Cultivo.objects.filter(idCultivo=datos[KEY_ID_CULTIVO], habilitado=True).__len__() == 0:
                raise ValueError(ERROR_CULTIVO_NO_HABILITADO, "El cultivo no está habilitado")
            cultivo_seleccionado = Cultivo.objects.get(idCultivo=datos[KEY_ID_CULTIVO])
            cultivo_seleccionado.habilitado = False
            cultivo_seleccionado.fechaEliminacion = datetime.now()
            cultivo_seleccionado.save()
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


# @transaction.atomic()
# @login_requerido
# @metodos_requeridos([METHOD_POST])
# def mostrar_cultivo_sector(request):
#     response = HttpResponse()
#     datos = obtener_datos_json(request)
#     try:
#         if Sector.objects.filter(idCultivo=datos[KEY_ID_SECTOR]).__len__() == 0:
#             raise ValueError(ERROR_SECTOR_NO_HABILITADO, "El id del cultivo no es correcto")
#         if Cultivo.objects.filter(idCultivo=datos[KEY_ID_CULTIVO], habilitado=True).__len__() == 0:
#             raise ValueError(ERROR_CULTIVO_NO_HABILITADO, "El cultivo no está habilitado")
#         cultivo_seleccionado = Cultivo.objects.get(idCultivo=datos[KEY_ID_CULTIVO])
#         response.content = armar_response_content(cultivo_seleccionado)
#         response.status_code = 200
#         return response
#     except ValueError as err:
#         print err.args
#         return build_bad_request_error(response, err.args[0], err.args[1])
#     except (IntegrityError, TypeError, KeyError) as err:
#         print err.args
#         response.status_code = 401
#         return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def mostrar_cultivo_sector(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if KEY_ID_SECTOR in datos:
            if datos[KEY_ID_SECTOR] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            estado_habilitado = EstadoSector.objects.get(nombreEstadoSector=ESTADO_HABILITADO)
            sector_seleccionado = Sector.objects.get(idSector=datos[KEY_ID_SECTOR])
            if HistoricoEstadoSector.objects.filter(sector=sector_seleccionado, estado_sector=estado_habilitado,
                                                    fechaFinEstadoSector__isnull=True).__len__() != 1:
                raise ValueError(ERROR_SECTOR_NO_HABILITADO, "El sector seleccionado no esta habilitado")
            if sector_seleccionado.cultivo_set.filter(habilitado=True).__len__() == 0 :
                response.content = "[]"
                response.status_code = 200
                return response
            cultivo_seleccionado = sector_seleccionado.cultivo_set.get(habilitado=True)
            response.content = armar_response_content(cultivo_seleccionado)
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
def mostrar_cultivo_sector_historico(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if KEY_ID_SECTOR in datos:
            if datos[KEY_ID_SECTOR] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            estado_habilitado = EstadoSector.objects.get(nombreEstadoSector=ESTADO_HABILITADO)
            sector_seleccionado = Sector.objects.get(idSector=datos[KEY_ID_SECTOR])
            if HistoricoEstadoSector.objects.filter(sector=sector_seleccionado, estado_sector=estado_habilitado,
                                                    fechaFinEstadoSector__isnull=True).__len__() != 1:
                raise ValueError(ERROR_SECTOR_NO_HABILITADO, "El sector seleccionado no esta habilitado")
            cultivo_seleccionado_lista = sector_seleccionado.cultivo_set.all()
            response.content = armar_response_list_content(cultivo_seleccionado_lista)
            response.status_code = 200
            return response
        else:
            raise ValueError(ERROR_SECTOR_NO_HABILITADO, "El sector seleccionado no esta habilitado")
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
def asignar_componente_sensor(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_ID_SECTOR in datos) and (KEY_ID_COMPONENTE_SENSOR in datos) and (KEY_ID_FINCA in datos):
            if datos[KEY_ID_SECTOR] == '' or datos[KEY_ID_COMPONENTE_SENSOR] == '' or datos[KEY_ID_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if Sector.objects.filter(idSector=datos[KEY_ID_SECTOR]).__len__() == 0:
                raise ValueError(ERROR_SECTOR_NO_ENCONTRADO, "No se encuentra un sector con ese id")
            estado_sector_habilitado = EstadoSector.objects.get(nombreEstadoSector=ESTADO_HABILITADO)
            sector_seleccionado = Sector.objects.get(idSector=datos[KEY_ID_SECTOR])
            if HistoricoEstadoSector.objects.filter(sector=sector_seleccionado, estado_sector=estado_sector_habilitado,
                                                    fechaFinEstadoSector__isnull=True).__len__() != 1:
                raise ValueError(ERROR_SECTOR_NO_HABILITADO, "El sector seleccionado no esta habilitado")
            if Finca.objects.filter(idFinca=datos[KEY_ID_FINCA]).__len__() != 1:
                raise ValueError(ERROR_FINCA_NO_ENCONTRADA, "No existe la finca ingresada")
            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
            if ComponenteSensor.objects.filter(idComponenteSensor=datos[KEY_ID_COMPONENTE_SENSOR],
                                               finca=finca).__len__() == 0:
                raise ValueError(ERROR_COMPONENTE_SENSOR_NO_PERTENECE_A_FINCA,
                                 "El componente no pertenece a la finca ingresada")
            if ComponenteSensor.objects.filter(idComponenteSensor=datos[KEY_ID_COMPONENTE_SENSOR]).__len__() == 0:
                raise ValueError(ERROR_COMPONENTE_SENSOR_NO_EXISTENTE, "No existe componente sensor con ese id")
            componente = ComponenteSensor.objects.get(idComponenteSensor=datos[KEY_ID_COMPONENTE_SENSOR])
            estado_componente_habilitado = EstadoComponenteSensor.objects.get(nombreEstado=ESTADO_HABILITADO)
            if componente.historico_estado_componente_sensor_list.filter(fechaFinEstadoComponenteSensor__isnull=True,
                                                                         estadoComponenteSensor=estado_componente_habilitado).__len__() == 0:
                raise ValueError(ERROR_COMPONENTE_SENSOR_NO_HABILITADO, "El componente no esta habilitado")
            if componente.componenteSensorSectorList.filter(habilitado=True).__len__() !=0:
                raise ValueError(ERROR_COMPONENTE_SENSOR_YA_ASIGNADO, "El componente ya esta asignado a otro sector")
            componente_sensor_sector = ComponenteSensorSector(componente_sensor=componente, sector=sector_seleccionado,
                                                              habilitado=True)
            estado_componente_sensor_sector_habilitado = EstadoComponenteSensorSector.objects.get(nombreEstadoComponenteSensorSector=ESTADO_HABILITADO)
            nuevo_historico = HistoricoEstadoComponenteSensorSector(estadoComponenteSensorSector=estado_componente_sensor_sector_habilitado,
                                                                    componenteSensorSector=componente_sensor_sector,
                                                                    fechaAltaComponenteSensorSector=datetime.now())
            componente_sensor_sector.save()
            nuevo_historico.save()
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
def desasignar_componente_sensor(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if  (KEY_ID_COMPONENTE_SENSOR in datos) and (KEY_ID_FINCA in datos):
            if  datos[KEY_ID_COMPONENTE_SENSOR] == '' or datos[KEY_ID_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if Finca.objects.filter(idFinca=datos[KEY_ID_FINCA]).__len__() != 1:
                raise ValueError(ERROR_FINCA_NO_ENCONTRADA, "No existe la finca ingresada")
            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
            if ComponenteSensor.objects.filter(idComponenteSensor=datos[KEY_ID_COMPONENTE_SENSOR],
                                               finca=finca).__len__() == 0:
                raise ValueError(ERROR_COMPONENTE_SENSOR_NO_PERTENECE_A_FINCA,
                                 "El componente no pertenece a la finca ingresada")

            if ComponenteSensor.objects.filter(idComponenteSensor=datos[KEY_ID_COMPONENTE_SENSOR]).__len__() == 0:
                raise ValueError(ERROR_COMPONENTE_SENSOR_NO_EXISTENTE, "No existe componente sensor con ese id")

            componente = ComponenteSensor.objects.get(idComponenteSensor=datos[KEY_ID_COMPONENTE_SENSOR])
            estado_componente_habilitado = EstadoComponenteSensor.objects.get(nombreEstado=ESTADO_HABILITADO)
            if componente.historico_estado_componente_sensor_list.filter(fechaFinEstadoComponenteSensor__isnull=True,
                                                                         estadoComponenteSensor=estado_componente_habilitado).__len__() == 0:
                raise ValueError(ERROR_COMPONENTE_SENSOR_NO_HABILITADO, "El componente no esta habilitado")
            if componente.componenteSensorSectorList.filter(habilitado=True).__len__() == 0 :
                raise ValueError(ERROR_COMPONENTE_SENSOR_NO_ASIGNADO, "No se puede desasignar al componente ya que no esta asignado")
            componente_sensor_sector = componente.componenteSensorSectorList.get(habilitado=True)
            estado_componente_sensor_deshabilitado = EstadoComponenteSensorSector.objects.get(nombreEstadoComponenteSensorSector=ESTADO_DESHABILITADO)
            historico_actual = componente_sensor_sector.historicoEstadoComponenteSensorSector.get(
                fechaBajaComponenteSensorSector__isnull=True)
            historico_actual.fechaBajaComponenteSensorSector = datetime.now()
            historico_actual.save()
            nuevo_historico = HistoricoEstadoComponenteSensorSector(estadoComponenteSensorSector=estado_componente_sensor_deshabilitado,
                                                                    componenteSensorSector=componente_sensor_sector,
                                                                    fechaAltaComponenteSensorSector=datetime.now())
            componente_sensor_sector.habilitado = False
            componente_sensor_sector.save()
            nuevo_historico.save()
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
