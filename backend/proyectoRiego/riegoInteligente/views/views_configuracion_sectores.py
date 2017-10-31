#-*- coding: UTF-8 -*-
from django.db import transaction
from .supportClases.security_decorators import *
from ..models import *
from supportClases.views_util_functions import *
from supportClases.error_handler import *
from supportClases.dto_modulo_configuracion_sectores import *


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_PUT])
@manejar_errores()
@permisos_rol_requeridos([PERMISO_PUEDECREARSECTOR])
def crear_sector(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_ID_FINCA in datos) and (KEY_NOMBRE_SECTOR in datos) and (KEY_DESCRIPCION_SECTOR in datos) and \
                (KEY_SUPERFICIE_SECTOR in datos):
            if datos[KEY_ID_FINCA] == '' or datos[KEY_NOMBRE_SECTOR] == '' or datos[KEY_DESCRIPCION_SECTOR] == '' \
                    or datos[KEY_SUPERFICIE_SECTOR] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if Finca.objects.filter(idFinca=datos[KEY_ID_FINCA]).__len__() == 0:
                raise ValueError(ERROR_FINCA_NO_ENCONTRADA, "No se encontro una finca con ese id.")
            finca_actual = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
            estado_finca_habilitado = EstadoFinca.objects.get(nombreEstadoFinca=ESTADO_HABILITADO)
            if finca_actual.historicoEstadoFincaList.get(fechaFinEstadoFinca__isnull=True).estadoFinca != \
                    estado_finca_habilitado:
                raise ValueError(ERROR_FINCA_NO_HABILITADA, "No se puede crear sector porque la finca no esta"
                                                            " habilitada.")
            estado_habilitado = EstadoSector.objects.get(nombreEstadoSector=ESTADO_HABILITADO)

            if Sector.objects.filter(numeroSector=datos[KEY_NUMERO_SECTOR], finca=finca_actual).__len__() != 0:
                sectores = Sector.objects.filter(numeroSector=datos[KEY_NUMERO_SECTOR], finca=finca_actual)
                for sector in sectores:
                    if sector.historicoEstadoSectorList.filter(fechaFinEstadoSector__isnull=True,
                                                               estado_sector=estado_habilitado).__len__() == 1:
                        raise ValueError(ERROR_SECTOR_YA_EXISTENTE, "Ya existe un sector con ese numero.")
            if Sector.objects.filter(nombreSector=datos[KEY_NOMBRE_SECTOR], finca=finca_actual).__len__() != 0:
                sectores = Sector.objects.filter(nombreSector=datos[KEY_NOMBRE_SECTOR], finca=finca_actual)
                for sector in sectores:
                    if sector.historicoEstadoSectorList.filter(fechaFinEstadoSector__isnull=True,
                                                               estado_sector=estado_habilitado).__len__() == 1:
                        raise ValueError(ERROR_SECTOR_YA_EXISTENTE, "Ya existe un sector con ese nombre.")
            if finca_actual.tamanio < float(datos[KEY_SUPERFICIE_SECTOR]):
                raise ValueError(ERROR_SECTOR_SUPERA_TAMANIO_FINCA, "El sector no puede ser mas grande que la finca.")
            superficie_ocupada = 0
            sectores_finca = Sector.objects.filter(finca=finca_actual)
            for sector in sectores_finca:
                if sector.historicoEstadoSectorList.filter(fechaFinEstadoSector__isnull=True,
                                                           estado_sector=estado_habilitado).__len__() == 1:
                    superficie_ocupada += float(sector.superficie)
            superficie_ocupada += float(datos[KEY_SUPERFICIE_SECTOR])
            if superficie_ocupada > finca_actual.tamanio:
                raise ValueError(ERROR_SECTORES_SUPERAN_TAMANIO_FINCA, "La suma de las superficies superan el tamanio"
                                                                       "de la finca.")
            if ConfiguracionEventoPersonalizado.objects.filter(nombre=HELADA).__len__() == 0:
                raise ValueError(ERROR_HELADA_NO_CARGADA, "No se encuentra cargada la configuracion para heladas.")
            helada = ConfiguracionEventoPersonalizado.objects.get(nombre=HELADA)
            usuario = request.user
            datos_usuario = usuario.datosusuario
            usuario_finca = UsuarioFinca.objects.get(usuario=datos_usuario, finca=finca_actual)
            usuario_finca.configuracionEventoPersonalizadoList.add(helada)
            usuario_finca.save()
            helada.save()
            sector_nuevo = Sector(numeroSector=datos[KEY_NUMERO_SECTOR], nombreSector=datos[KEY_NOMBRE_SECTOR],
                                  descripcionSector=datos[KEY_DESCRIPCION_SECTOR],
                                  superficie=int(datos[KEY_SUPERFICIE_SECTOR]),
                                  finca=finca_actual
                                  )
            sector_nuevo.save()
            historico_nuevo = HistoricoEstadoSector(estado_sector=estado_habilitado, sector=sector_nuevo,
                                                    fechaInicioEstadoSector=datetime.now(pytz.utc))
            historico_nuevo.save()
            helada.sectorList.add(sector_nuevo)
            helada.save()
            finca_actual.save()
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
@permisos_rol_requeridos([PERMISO_PUEDEGESTIONARSECTOR])
def modificar_sector(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_ID_SECTOR in datos) and (KEY_NOMBRE_SECTOR in datos) and (KEY_DESCRIPCION_SECTOR in datos) and\
                (KEY_SUPERFICIE_SECTOR in datos):
            if datos[KEY_ID_SECTOR] == '' or datos[KEY_NOMBRE_SECTOR] == '' or datos[KEY_DESCRIPCION_SECTOR] == ''\
                    or datos[KEY_SUPERFICIE_SECTOR] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            sector_seleccionado = Sector.objects.get(idSector=datos[KEY_ID_SECTOR])
            estado_habilitado = EstadoSector.objects.get(nombreEstadoSector=ESTADO_HABILITADO)
            if HistoricoEstadoSector.objects.filter(sector=sector_seleccionado, estado_sector=estado_habilitado,
                                                    fechaFinEstadoSector__isnull=True).__len__() != 1:
                raise ValueError(ERROR_SECTOR_NO_HABILITADO, "El sector seleccionado no esta habilitado")
            finca_actual = sector_seleccionado.finca
            if finca_actual.tamanio < float(datos[KEY_SUPERFICIE_SECTOR]):
                raise ValueError(ERROR_SECTOR_SUPERA_TAMANIO_FINCA, "El sector no puede ser mas grande que la finca.")
            superficie_ocupada = 0
            sectores_finca = Sector.objects.filter(finca=finca_actual)
            for sector in sectores_finca:
                if sector.historicoEstadoSectorList.filter(fechaFinEstadoSector__isnull=True,
                                                           estado_sector=estado_habilitado).__len__() == 1:
                    superficie_ocupada += float(sector.superficie)
            superficie_ocupada += float(datos[KEY_SUPERFICIE_SECTOR])-sector.superficie
            if superficie_ocupada > finca_actual.tamanio:
                raise ValueError(ERROR_SECTORES_SUPERAN_TAMANIO_FINCA, "La suma de las superficies superan el tamanio"
                                                                       "de la finca.")
            sector_seleccionado.nombreSector = datos[KEY_NOMBRE_SECTOR]
            sector_seleccionado.descripcionSector = datos[KEY_DESCRIPCION_SECTOR]
            sector_seleccionado.superficie = datos[KEY_SUPERFICIE_SECTOR]
            sector_seleccionado.save()
            response.content = armar_response_content(None)
            response.status_code = 200
            return response
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
    except ValueError as err:
        return build_bad_request_error(response, err.args[0], err.args[1])
    except (IntegrityError, TypeError, KeyError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
@manejar_errores()
@permisos_rol_requeridos([PERMISO_PUEDEGESTIONARSECTOR])
def eliminar_sector(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if KEY_ID_SECTOR in datos:
            if datos[KEY_ID_SECTOR] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if Sector.objects.filter(idSector=datos[KEY_ID_SECTOR]).__len__() == 0:
                raise ValueError(ERROR_SECTOR_NO_ENCONTRADO, "No se encontro a un sector con ese id")
            sector_seleccionado = Sector.objects.get(idSector=datos[KEY_ID_SECTOR])
            estado_habilitado = EstadoSector.objects.get(nombreEstadoSector=ESTADO_HABILITADO)
            if HistoricoEstadoSector.objects.filter(sector=sector_seleccionado, estado_sector=estado_habilitado,
                                                    fechaFinEstadoSector__isnull=True).__len__() != 1:
                raise ValueError(ERROR_SECTOR_NO_HABILITADO, "El sector seleccionado no esta habilitado")
            estado_mecanismo_riego_finca_sector_habilitado = EstadoMecanismoRiegoFincaSector.objects.get(
                nombreEstadoMecanismoRiegoFincaSector=ESTADO_HABILITADO)
            mecanismo_riego_sector_a_deshabilitar = ""
            if sector_seleccionado.mecanismoRiegoFincaSector.all().__len__() > 0:
                for mecanismo in sector_seleccionado.mecanismoRiegoFincaSector.all():
                    if mecanismo.historicoMecanismoRiegoFincaSector.filter(
                            estado_mecanismo_riego_finca_sector=estado_mecanismo_riego_finca_sector_habilitado,
                            fechaFinEstadoMecanismoRiegoFincaSector__isnull=True).__len__() == 1:
                        mecanismo_riego_sector_a_deshabilitar = mecanismo

            if mecanismo_riego_sector_a_deshabilitar != "":
                estado_ejecucion_riego = EstadoEjecucionRiego.objects.get(nombreEstadoEjecucionRiego=ESTADO_EN_EJECUCION)
                lista_riegos = mecanismo_riego_sector_a_deshabilitar.ejecucionRiegoList.filter(
                    estado_ejecucion_riego=estado_ejecucion_riego)
                if lista_riegos.__len__() > 0:
                    raise ValueError(ERROR_RIEGO_EN_EJECUCION, "No se puede eliminar el sector porque hay un riego "
                                                               "en ejecucion, espere a que termine el riego.")

            historico_viejo = HistoricoEstadoSector.objects.get(sector=sector_seleccionado,
                                                                estado_sector=estado_habilitado,
                                                                fechaFinEstadoSector__isnull=True)
            historico_viejo.fechaFinEstadoSector = datetime.now(pytz.utc)
            historico_viejo.save()
            estado_deshabilitado = EstadoSector.objects.get(nombreEstadoSector=ESTADO_DESHABILITADO)
            historico_nuevo = HistoricoEstadoSector(fechaInicioEstadoSector=datetime.now(pytz.utc),
                                                    estado_sector=estado_deshabilitado)
            sector_seleccionado.historicoEstadoSectorList.add(historico_nuevo, bulk=False)
            sector_seleccionado.save()
            mecanismo_riego_sector_lista = MecanismoRiegoFincaSector.objects.filter(sector=sector_seleccionado)
            estado_mecanismo_riego_sector_habilitado = EstadoMecanismoRiegoFincaSector.objects.get(
                nombreEstadoMecanismoRiegoFincaSector=ESTADO_HABILITADO)
            estado_mecanismo_riego_sector_deshabilitado = EstadoMecanismoRiegoFincaSector.objects.get(
                nombreEstadoMecanismoRiegoFincaSector=ESTADO_DESHABILITADO)
            estado_configuracion_riego_habilitada = EstadoConfiguracionRiego.objects.get(
                nombreEstadoConfiguracionRiego=ESTADO_HABILITADO)
            estado_configuracion_riego_deshabilitada = EstadoConfiguracionRiego.objects.get(
                nombreEstadoConfiguracionRiego=ESTADO_DESHABILITADO)
            for mecanismo_riego_sector in mecanismo_riego_sector_lista:
                if mecanismo_riego_sector.historicoMecanismoRiegoFincaSector.filter(
                        fechaFinEstadoMecanismoRiegoFincaSector__isnull=True,
                        estado_mecanismo_riego_finca_sector=estado_mecanismo_riego_sector_habilitado).__len__() == 1:
                    mecanismo_riego_sector_deshabilitar = mecanismo_riego_sector
                    ultimo_historico_mecanismo_riego_sector = mecanismo_riego_sector. \
                        historicoMecanismoRiegoFincaSector.get(
                        fechaFinEstadoMecanismoRiegoFincaSector__isnull=True,
                        estado_mecanismo_riego_finca_sector=estado_mecanismo_riego_sector_habilitado)
                    ultimo_historico_mecanismo_riego_sector.fechaFinEstadoMecanismoRiegoFincaSector = \
                        datetime.now(pytz.utc)
                    ultimo_historico_mecanismo_riego_sector.save()
                    nuevo_historico_mecanismo_riego_sector = HistoricoMecanismoRiegoFincaSector(
                        mecanismo_riego_finca_sector=mecanismo_riego_sector_deshabilitar,
                        fechaInicioEstadoMecanismoRiegoFincaSector=datetime.now(pytz.utc),
                        estado_mecanismo_riego_finca_sector=estado_mecanismo_riego_sector_deshabilitado)
                    nuevo_historico_mecanismo_riego_sector.save()
                    lista_configuraciones_riego = mecanismo_riego_sector.configuracionriego_set.all()
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

            if sector_seleccionado.componentesensorsector_set.filter(habilitado=True).__len__() == 1:
                componente_sensor_sector = sector_seleccionado.componentesensorsector_set.get(habilitado=True)
                ultimo_historico_componente_sensor_sector = componente_sensor_sector.\
                    historicoEstadoComponenteSensorSector.get(fechaBajaComponenteSensorSector__isnull=True)
                estado_componente_sensor_deshabilitado = EstadoComponenteSensorSector.objects.get(
                    nombreEstadoComponenteSensorSector=ESTADO_DESHABILITADO)
                ultimo_historico_componente_sensor_sector.fechaBajaComponenteSensorSector = datetime.now(pytz.utc)
                ultimo_historico_componente_sensor_sector.save()
                nuevo_historico = HistoricoEstadoComponenteSensorSector(
                    estadoComponenteSensorSector=estado_componente_sensor_deshabilitado,
                    componenteSensorSector=componente_sensor_sector,
                    fechaAltaComponenteSensorSector=datetime.now(pytz.utc))
                componente_sensor_sector.habilitado = False
                componente_sensor_sector.save()
                nuevo_historico.save()
            response.content = armar_response_content(None)
            response.status_code = 200
            return response
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
    except ValueError as err:
        return build_bad_request_error(response, err.args[0], err.args[1])
    except (IntegrityError, TypeError, KeyError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
@manejar_errores()
def mostrar_sectores(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if KEY_ID_FINCA in datos:
            if datos[KEY_ID_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            finca_actual = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
            estado_habilitado = EstadoSector.objects.get(nombreEstadoSector=ESTADO_HABILITADO)
            lista_sectores = Sector.objects.filter(finca=finca_actual)
            sectores_habilitados = []
            for sector in lista_sectores:
                if HistoricoEstadoSector.objects.filter(sector=sector, fechaFinEstadoSector__isnull=True,
                                                        estado_sector=estado_habilitado).__len__() == 1:
                        sectores_habilitados.append(sector)

            response.content = armar_response_list_content(sectores_habilitados)
            response.status_code = 200
            return response
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
    except ValueError as err:
        return build_bad_request_error(response, err.args[0], err.args[1])
    except (IntegrityError, TypeError, KeyError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
@manejar_errores()
def buscar_sector_id(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if KEY_ID_SECTOR in datos:
            if datos[KEY_ID_SECTOR] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if Sector.objects.filter(idSector=datos[KEY_ID_SECTOR]).__len__() == 0:
                raise ValueError(ERROR_SECTOR_NO_ENCONTRADO, "No se encontro a un sector con ese id")
            sector = Sector.objects.get(idSector=datos[KEY_ID_SECTOR])
            response.content = armar_response_content(sector)
            return response
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
    except (ValueError, IntegrityError) as err:
        print err.args
        response.content = err.args


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def mostrar_mecanismo_riego_sector(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if KEY_ID_SECTOR in datos:
            if datos[KEY_ID_SECTOR] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if Sector.objects.filter(idSector=datos[KEY_ID_SECTOR]).__len__() == 0:
                raise ValueError(ERROR_SECTOR_NO_ENCONTRADO, "No se encuentra un sector con ese id")
            estado_habilitado = EstadoSector.objects.get(nombreEstadoSector=ESTADO_HABILITADO)
            sector_seleccionado = Sector.objects.get(idSector=datos[KEY_ID_SECTOR])
            if HistoricoEstadoSector.objects.filter(sector=sector_seleccionado, estado_sector=estado_habilitado,
                                                    fechaFinEstadoSector__isnull=True).__len__() != 1:
                raise ValueError(ERROR_SECTOR_NO_HABILITADO, "El sector seleccionado no esta habilitado")
            estado_mecanismo_sector_habilitado = EstadoMecanismoRiegoFincaSector.objects.get(
                nombreEstadoMecanismoRiegoFincaSector=ESTADO_HABILITADO)
            mecanismo_sector_lista = sector_seleccionado.mecanismoRiegoFincaSector.all()
            for mecanismo in mecanismo_sector_lista:
                if mecanismo.historicoMecanismoRiegoFincaSector.filter(
                        estado_mecanismo_riego_finca_sector=estado_mecanismo_sector_habilitado,
                        fechaFinEstadoMecanismoRiegoFincaSector__isnull=True).__len__() == 1:
                    response.content = armar_response_content(mecanismo)
                    response.status_code = 200
                    return response
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
@permisos_rol_requeridos([PERMISO_PUEDEGESTIONARSECTOR, PERMISO_PUEDEASIGNARMECRIEGOASECTOR])
def asignar_mecanismo_a_sector(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_ID_SECTOR in datos) and (KEY_ID_MECANISMO_RIEGO_FINCA in datos):
            if datos[KEY_ID_SECTOR] == '' or datos[KEY_ID_MECANISMO_RIEGO_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            sector_seleccionado = Sector.objects.get(idSector=datos[KEY_ID_SECTOR])
            mecanismo_riego_sector_lista = sector_seleccionado.mecanismoRiegoFincaSector.all()
            estado_mecanismo_riego_finca_sector_habilitado = EstadoMecanismoRiegoFincaSector.objects.get(
                nombreEstadoMecanismoRiegoFincaSector=ESTADO_HABILITADO)
            for mecanismo_sector in mecanismo_riego_sector_lista:
                if HistoricoMecanismoRiegoFincaSector.objects.filter(
                        fechaFinEstadoMecanismoRiegoFincaSector__isnull=True,
                        mecanismo_riego_finca_sector=mecanismo_sector,
                        estado_mecanismo_riego_finca_sector=estado_mecanismo_riego_finca_sector_habilitado) \
                        .__len__() != 0:
                    raise ValueError(ERROR_SECTOR_YA_TIENE_MECANISMO_HABILITADO,
                                     "El sector ya tiene un mecanismo de riego asignado")
            mecanismo_riego_finca_seleccionado = MecanismoRiegoFinca.objects.get(
                idMecanismoRiegoFinca=datos[KEY_ID_MECANISMO_RIEGO_FINCA])
            historico_mecanismo_riego_finca_actual = mecanismo_riego_finca_seleccionado.\
                historicoMecanismoRiegoFincaList.get(fechaFinEstadoMecanismoRiegoFinca__isnull=True)
            if historico_mecanismo_riego_finca_actual.estado_mecanismo_riego_finca.nombreEstadoMecanismoRiegoFinca \
                    != ESTADO_HABILITADO:
                raise ValueError(ERROR_MECANISMO_RIEGO_FINCA_NO_HABILITADO,
                                 "El mecanismo seleccionado no se encuentra habilitado para la finca")
            historico_sector_seleccionado_actual = sector_seleccionado.historicoEstadoSectorList.get(
                fechaFinEstadoSector__isnull=True)
            if historico_sector_seleccionado_actual.estado_sector.nombreEstadoSector != ESTADO_HABILITADO:
                raise ValueError(ERROR_SECTOR_NO_HABILITADO, "El sector seleccionado no se encuentra habilitado")
            mecanismo_riego_sector = MecanismoRiegoFincaSector(mecanismoRiegoFinca=mecanismo_riego_finca_seleccionado,
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
            nuevo_historico = HistoricoMecanismoRiegoFincaSector(
                fechaInicioEstadoMecanismoRiegoFincaSector=datetime.now(pytz.utc),
                estado_mecanismo_riego_finca_sector=estado_mecanismo_riego_finca_sector_habilitado)
            mecanismo_riego_sector.historicoMecanismoRiegoFincaSector.add(nuevo_historico, bulk=False)
            mecanismo_riego_sector.save()
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
@permisos_rol_requeridos([PERMISO_PUEDEGESTIONARSECTOR, PERMISO_PUEDEASIGNARMECRIEGOASECTOR])
def deshabilitar_mecanismo_riego_sector(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR in datos:
            if datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if MecanismoRiegoFincaSector.objects.filter(
                    idMecanismoRiegoFincaSector=datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR]).__len__() == 0:
                raise ValueError(ERROR_MECANISMO_RIEGO_FINCA_SECTOR_NO_EXISTE,
                                 "El idMecanismoRiegoFincaSector no existe")
            mecanismo_riego_finca_sector = MecanismoRiegoFincaSector.objects.get(
                idMecanismoRiegoFincaSector=datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR])
            estado_mecanismo_sector_habilitado = EstadoMecanismoRiegoFincaSector.objects.get(
                nombreEstadoMecanismoRiegoFincaSector=ESTADO_HABILITADO)
            if HistoricoMecanismoRiegoFincaSector.objects.filter(
                    mecanismo_riego_finca_sector=mecanismo_riego_finca_sector,
                    fechaFinEstadoMecanismoRiegoFincaSector__isnull=True,
                    estado_mecanismo_riego_finca_sector=estado_mecanismo_sector_habilitado).__len__() != 1:
                raise ValueError(ERROR_MECANISMO_RIEGO_FINCA_SECTOR_NO_HABILITADO, "El mecanismo sector no se encuentra"
                                                                                   " habilitado")
            estado_ejecucion_riego = EstadoEjecucionRiego.objects.get(nombreEstadoEjecucionRiego=ESTADO_EN_EJECUCION)
            lista_riegos = mecanismo_riego_finca_sector.ejecucionRiegoList.filter(
                estado_ejecucion_riego=estado_ejecucion_riego)
            if lista_riegos.__len__() > 0:
                raise ValueError(ERROR_RIEGO_EN_EJECUCION, "No se puede desasignar el mecanismo porque hay un riego "
                                                           "en ejecucion, espere a que termine el riego.")
            estado_configuracion_riego_habilitada = EstadoConfiguracionRiego.objects.get(
                nombreEstadoConfiguracionRiego=ESTADO_HABILITADO)
            estado_configuracion_riego_deshabilitada = EstadoConfiguracionRiego.objects.get(
                nombreEstadoConfiguracionRiego=ESTADO_DESHABILITADO)
            lista_configuraciones_riego = mecanismo_riego_finca_sector.configuracionriego_set.all()
            for configuracion in lista_configuraciones_riego:
                if configuracion.historicoEstadoConfiguracionRiegoList.filter(
                        estado_configuracion_riego=estado_configuracion_riego_habilitada,
                        fechaFinEstadoConfiguracionRiego__isnull=True).__len__() == 1:
                    ultimo_historico_configuracion_riego = configuracion.historicoEstadoConfiguracionRiegoList. \
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

            ultimo_historico_mecanismo_finca_sector = HistoricoMecanismoRiegoFincaSector.objects.get(
                mecanismo_riego_finca_sector=mecanismo_riego_finca_sector,
                fechaFinEstadoMecanismoRiegoFincaSector__isnull=True,
                estado_mecanismo_riego_finca_sector=estado_mecanismo_sector_habilitado)
            ultimo_historico_mecanismo_finca_sector.fechaFinEstadoMecanismoRiegoFincaSector = datetime.now(pytz.utc)
            ultimo_historico_mecanismo_finca_sector.save()
            estado_mecanismo_finca_sector_deshabilitado = EstadoMecanismoRiegoFincaSector.objects.get(
                nombreEstadoMecanismoRiegoFincaSector=ESTADO_DESHABILITADO)
            nuevo_historico_mecanismo_finca_sector = HistoricoMecanismoRiegoFincaSector(
                estado_mecanismo_riego_finca_sector=estado_mecanismo_finca_sector_deshabilitado,
                fechaInicioEstadoMecanismoRiegoFincaSector=datetime.now(pytz.utc),
                mecanismo_riego_finca_sector=mecanismo_riego_finca_sector)
            nuevo_historico_mecanismo_finca_sector.save()
            mecanismo_riego_finca_sector.save()
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
@metodos_requeridos([METHOD_GET])
@manejar_errores()
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
@manejar_errores()
@permisos_rol_requeridos([PERMISO_PUEDEGESTIONARSECTOR, PERMISO_PUEDEASIGNARCULTIVO])
def asignar_cultivo_a_sector(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_ID_SECTOR in datos) and (KEY_DESCRIPCION_CULTIVO in datos) and (KEY_FECHA_PLANTACION in datos) and\
                (KEY_NOMBRE_SUBTIPO_CULTIVO in datos) and (KEY_NOMBRE_CULTIVO in datos) and (KEY_CANTIDAD_PLANTAS)\
                in datos:
            if datos[KEY_ID_SECTOR] == '' or datos[KEY_DESCRIPCION_CULTIVO] == '' or datos[KEY_FECHA_PLANTACION] == ''\
                    or datos[KEY_NOMBRE_CULTIVO] == '' or datos[KEY_NOMBRE_SUBTIPO_CULTIVO] == '' or datos[KEY_CANTIDAD_PLANTAS] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            sector_seleccionado = Sector.objects.get(idSector=datos[KEY_ID_SECTOR])
            if sector_seleccionado.cultivo_set.all() is None:
                if sector_seleccionado.cultivo_set.filter(habilitado=True).__len__() != 0:
                    raise ValueError(ERROR_SECTOR_YA_TIENE_CULTIVO_ASIGNADO, "El sector ya tiene un cultivo asignado")
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
            if not subtipo_seleccionado.tipo_cultivo.habilitado:
                raise ValueError(ERROR_TIPO_CULTIVO_NO_HABILITADO, "Este tipo de cultivo no esta habilitado")
            fecha_parseada = parsear_datos_fecha_a_utc(datos[KEY_FECHA_PLANTACION])
            cultivo = Cultivo(nombre=datos[KEY_NOMBRE_CULTIVO],
                              descripcion=datos[KEY_DESCRIPCION_CULTIVO],
                              habilitado=True,
                              sector=sector_seleccionado,
                              fechaPlantacion=fecha_parseada,
                              cantidad_plantas_hectarea=datos[KEY_CANTIDAD_PLANTAS],
                              subtipo_cultivo=subtipo_seleccionado)
            cultivo.save()
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
@permisos_rol_requeridos([PERMISO_PUEDEGESTIONARSECTOR, PERMISO_PUEDEASIGNARCULTIVO])
def modificar_cultivo_sector(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_ID_CULTIVO in datos) and (KEY_DESCRIPCION_CULTIVO in datos) and (KEY_FECHA_PLANTACION in datos)\
                and (KEY_NOMBRE_CULTIVO in datos) and (KEY_CANTIDAD_PLANTAS in datos):
            if datos[KEY_ID_CULTIVO] == '' or datos[KEY_DESCRIPCION_CULTIVO] == '' or\
                            datos[KEY_FECHA_PLANTACION] == '' or datos[KEY_NOMBRE_CULTIVO] == ''\
                    or datos[KEY_CANTIDAD_PLANTAS] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if Cultivo.objects.filter(idCultivo=datos[KEY_ID_CULTIVO]).__len__() == 0:
                raise ValueError(ERROR_CULTIVO_NO_EXISTENTE, "El id del cultivo no es correcto")
            if Cultivo.objects.filter(idCultivo=datos[KEY_ID_CULTIVO], habilitado=True).__len__() == 0:
                raise ValueError(ERROR_CULTIVO_NO_HABILITADO, "El cultivo no está habilitado")
            cultivo_seleccionado = Cultivo.objects.get(idCultivo=datos[KEY_ID_CULTIVO])
            cultivo_seleccionado.descripcion = datos[KEY_DESCRIPCION_CULTIVO]
            cultivo_seleccionado.fechaPlantacion = datos[KEY_FECHA_PLANTACION]
            cultivo_seleccionado.nombre = datos[KEY_NOMBRE_CULTIVO]
            cultivo_seleccionado.cantidad_plantas_hectarea = datos[KEY_CANTIDAD_PLANTAS]
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

@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
@manejar_errores()
@permisos_rol_requeridos([PERMISO_PUEDEGESTIONARSECTOR, PERMISO_PUEDEASIGNARCULTIVO])
def buscar_cultivo_id(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if KEY_ID_CULTIVO in datos:
            if datos[KEY_ID_CULTIVO]:
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if Cultivo.objects.filter(idCultivo=datos[KEY_ID_CULTIVO]).__len__() == 0:
                raise ValueError(ERROR_CULTIVO_NO_EXISTENTE, "El id del cultivo no es correcto")
            if Cultivo.objects.filter(idCultivo=datos[KEY_ID_CULTIVO], habilitado=True).__len__() == 0:
                raise ValueError(ERROR_CULTIVO_NO_HABILITADO, "El cultivo no está habilitado")
            cultivo_seleccionado = Cultivo.objects.get(idCultivo=datos[KEY_ID_CULTIVO])
            response.content = armar_response_content(cultivo)
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
@permisos_rol_requeridos([PERMISO_PUEDEGESTIONARSECTOR, PERMISO_PUEDEASIGNARCULTIVO])
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
            cultivo_seleccionado.fechaEliminacion = datetime.now(pytz.utc)
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
@manejar_errores()
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
            if sector_seleccionado.cultivo_set.filter(habilitado=True).__len__() == 0:
                response.content = armar_response_content(None)
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
@manejar_errores()
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
@manejar_errores()
def mostrar_componente_sensor_sector(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if KEY_ID_SECTOR in datos:
            if datos[KEY_ID_SECTOR] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if Sector.objects.filter(idSector=datos[KEY_ID_SECTOR]).__len__() == 0:
                raise ValueError(ERROR_SECTOR_NO_ENCONTRADO, "No se encuentra un sector con ese id")
            estado_sector_habilitado = EstadoSector.objects.get(nombreEstadoSector=ESTADO_HABILITADO)
            sector_seleccionado = Sector.objects.get(idSector=datos[KEY_ID_SECTOR])
            if HistoricoEstadoSector.objects.filter(sector=sector_seleccionado, estado_sector=estado_sector_habilitado,
                                                    fechaFinEstadoSector__isnull=True).__len__() != 1:
                raise ValueError(ERROR_SECTOR_NO_HABILITADO, "El sector seleccionado no esta habilitado")
            if sector_seleccionado.componentesensorsector_set.filter(habilitado=True).__len__() == 0:
                response.content = armar_response_content(None)
                response.status_code = 200
                return response
            componente_sensor_sector = sector_seleccionado.componentesensorsector_set.get(habilitado=True)
            componente_sensor = componente_sensor_sector.componente_sensor
            response.content = armar_response_content(componente_sensor)
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
@permisos_rol_requeridos([PERMISO_PUEDEGESTIONARSECTOR, PERMISO_PUEDEASIGNARCOMPONENTESENSOR])
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
            if sector_seleccionado.componentesensorsector_set.filter(habilitado=True).__len__() != 0:
                raise ValueError(ERROR_SECTOR_YA_TIENE_COMPONENTE_HABILITADO,
                                 "El sector ya tiene un componente asignado")
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
            if componente.historico_estado_componente_sensor_list.filter(
                    fechaFinEstadoComponenteSensor__isnull=True,
                    estadoComponenteSensor=estado_componente_habilitado).__len__() == 0:
                raise ValueError(ERROR_COMPONENTE_SENSOR_NO_HABILITADO, "El componente no esta habilitado")
            if componente.componenteSensorSectorList.filter(habilitado=True).__len__() != 0:
                raise ValueError(ERROR_COMPONENTE_SENSOR_YA_ASIGNADO, "El componente ya esta asignado a otro sector")
            componente_sensor_sector = ComponenteSensorSector(componente_sensor=componente, sector=sector_seleccionado,
                                                              habilitado=True)
            estado_componente_sensor_sector_habilitado = EstadoComponenteSensorSector.objects.get(
                nombreEstadoComponenteSensorSector=ESTADO_HABILITADO)
            nuevo_historico = HistoricoEstadoComponenteSensorSector(
                estadoComponenteSensorSector=estado_componente_sensor_sector_habilitado,
                componenteSensorSector=componente_sensor_sector,
                fechaAltaComponenteSensorSector=datetime.now(pytz.utc))
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
@manejar_errores()
@permisos_rol_requeridos([PERMISO_PUEDEGESTIONARSECTOR, PERMISO_PUEDEASIGNARCOMPONENTESENSOR])
def desasignar_componente_sensor(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if(KEY_ID_COMPONENTE_SENSOR in datos) and (KEY_ID_FINCA in datos):
            if datos[KEY_ID_COMPONENTE_SENSOR] == '' or datos[KEY_ID_FINCA] == '':
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
            if componente.componenteSensorSectorList.filter(habilitado=True).__len__() == 0:
                raise ValueError(ERROR_COMPONENTE_SENSOR_NO_ASIGNADO_A_SECTOR,
                                 "No se puede desasignar al componente ya que no esta asignado")
            componente_sensor_sector = componente.componenteSensorSectorList.get(habilitado=True)
            estado_componente_sensor_deshabilitado = EstadoComponenteSensorSector.objects.get(
                nombreEstadoComponenteSensorSector=ESTADO_DESHABILITADO)
            historico_actual = componente_sensor_sector.historicoEstadoComponenteSensorSector.get(
                fechaBajaComponenteSensorSector__isnull=True)
            historico_actual.fechaBajaComponenteSensorSector = datetime.now(pytz.utc)
            historico_actual.save()
            nuevo_historico = HistoricoEstadoComponenteSensorSector(
                estadoComponenteSensorSector=estado_componente_sensor_deshabilitado,
                componenteSensorSector=componente_sensor_sector,
                fechaAltaComponenteSensorSector=datetime.now(pytz.utc))
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
