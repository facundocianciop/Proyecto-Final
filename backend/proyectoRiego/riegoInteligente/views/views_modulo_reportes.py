# -*- coding: UTF-8 -*-
from django.db import IntegrityError, transaction
from .supportClases.security_decorators import *
from ..models import *
from .supportClases.dto_modulo_reportes import *
from supportClases.views_util_functions import *
from supportClases.error_handler import *


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def buscar_configuraciones_eventos_personalizados(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_ID_USUARIO_FINCA in datos):
            if  datos[KEY_ID_USUARIO_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if UsuarioFinca.objects.filter(idUsuarioFinca=datos[KEY_ID_USUARIO_FINCA]).__len__() == 0:
                raise ValueError(ERROR_USUARIO_FINCA_NO_ENCONTRADO, "No se encuentra un usuario finca con ese id")
            if UsuarioFinca.objects.filter(idUsuarioFinca=datos[KEY_ID_USUARIO_FINCA],
                                           fechaBajaUsuarioFinca__isnull=True).__len__() == 0:
                raise ValueError(ERROR_USUARIO_NO_HABILITADO_EN_FINCA, "El usuario no esta habilitado en esa finca")
            usuario_finca = UsuarioFinca.objects.get(idUsuarioFinca=datos[KEY_ID_USUARIO_FINCA])
            lista_configuraciones_eventos_personalizados = usuario_finca.configuracionEventoList.all()
            lista_dto_configuracion_eventos = []
            for configuracion in lista_configuraciones_eventos_personalizados:
                lista_medicion_interna_json = []
                lista_medicion_externa_json= []
                for  medicion in configuracion.medicionEventoList.all():
                    if type(medicion) is MedicionFuenteInterna:
                        lista_medicion_interna_json.append(medicion.as_json())
                    elif type(medicion) is MedicionEstadoExterno:
                        lista_medicion_externa_json.append(medicion.as_json())
                dto_configuracion_evento = DtoConfiguracionEventoPersonalizado(idConfiguracionEvento=configuracion.idConfiguracion,
                                                                               nombre=configuracion.nombre,
                                                                               descripcion=configuracion.descripcion,
                                                                               fechaHoraCreacion=configuracion.fechaHoraCreacion,
                                                                               activado=configuracion.activado,
                                                                               numeroSector=configuracion.sector.numeroSector,
                                                                               idSector=configuracion.sector.idSector,
                                                                               notificacionActivada=configuracion.notificacionActivada,
                                                                               listaMedicionesInterna=lista_medicion_interna_json,
                                                                               listaMedicionesExternas=lista_medicion_externa_json
                                                                               )
                lista_dto_configuracion_eventos.append(dto_configuracion_evento)
            response.content = armar_response_list_content(lista_dto_configuracion_eventos)
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
def mostrar_configuracion_evento_personalizado(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_ID_CONFIGURACION_EVENTO_PERSONALIZADO in datos):
            if  datos[KEY_ID_CONFIGURACION_EVENTO_PERSONALIZADO] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if ConfiguracionEventoPersonalizado.objects.filter(
                    idConfiguracion=datos[KEY_ID_CONFIGURACION_EVENTO_PERSONALIZADO]).__len__() == 0:
                raise ValueError(ERROR_CONFIGURACION_EVENTO_NO_ENCONTRADA,
                                 "No se encuentra una configuracion con ese id")
            configuracion = ConfiguracionEventoPersonalizado.objects.get(
                    idConfiguracion=datos[KEY_ID_CONFIGURACION_EVENTO_PERSONALIZADO])
            lista_medicion_interna_json = []
            lista_medicion_externa_json = []
            for medicion in configuracion.medicionEventoList.all():
                if isinstance(medicion, MedicionFuenteInterna):
                    lista_medicion_interna_json.append(medicion.as_json())
                elif isinstance(medicion, MedicionEstadoExterno):
                    lista_medicion_externa_json.append(medicion.as_json())
            dto_configuracion_evento = DtoConfiguracionEventoPersonalizado(idConfiguracionEvento=configuracion.idConfiguracion,
                                                                           nombre=configuracion.nombre,
                                                                           descripcion=configuracion.descripcion,
                                                                           fechaHoraCreacion=configuracion.fechaHoraCreacion,
                                                                           activado=configuracion.activado,
                                                                           numeroSector=configuracion.sector.numeroSector,
                                                                           idSector=configuracion.sector.idSector,
                                                                           notificacionActivada=configuracion.notificacionActivada,
                                                                           listaMedicionesInterna=lista_medicion_interna_json,
                                                                           listaMedicionesExternas=lista_medicion_externa_json)
            response.content = armar_response_content(dto_configuracion_evento)
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
def mostrar_tipo_medicion_interna_finca(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_ID_FINCA in datos):
            if  datos[KEY_ID_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if Finca.objects.filter(idFinca=datos[KEY_ID_FINCA]).__len__() == 0:
                raise ValueError(ERROR_FINCA_NO_ENCONTRADA, "No se encuentra una finca con ese id")
            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
            estado_finca_deshabilitado = EstadoFinca.objects.get(nombreEstadoFinca=ESTADO_HABILITADO)
            if finca.historicoEstadoFincaList.filter(fechaFinEstadoFinca__isnull=True,
                                                            estadoFinca= estado_finca_deshabilitado).__len__() == 0:
                raise ValueError(ERROR_FINCA_NO_HABILITADA, "La finca no esta habilitada")
            sensores_habilitados = finca.sensor_set.filter(habilitado=True)
            lista_tipo_medicion = []
            for sensor in sensores_habilitados:
                if sensor.tipoMedicion.habilitado:
                    tipo_medicion = sensor.tipoMedicion
                    if lista_tipo_medicion.__contains__(tipo_medicion) == False:
                        lista_tipo_medicion.append(tipo_medicion)
            response.content = armar_response_list_content(lista_tipo_medicion)
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
def mostrar_tipo_medicion_climatica_finca(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_ID_FINCA in datos):
            if  datos[KEY_ID_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if Finca.objects.filter(idFinca=datos[KEY_ID_FINCA]).__len__() == 0:
                raise ValueError(ERROR_FINCA_NO_ENCONTRADA, "No se encuentra una finca con ese id")
            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
            estado_finca_deshabilitado = EstadoFinca.objects.get(nombreEstadoFinca=ESTADO_HABILITADO)
            if finca.historicoEstadoFincaList.filter(fechaFinEstadoFinca__isnull=True,
                                                            estadoFinca= estado_finca_deshabilitado).__len__() == 0:
                raise ValueError(ERROR_FINCA_NO_HABILITADA, "La finca no esta habilitada")
            if  finca.proveedorinformacionclimaticafinca_set.filter(
                fechaBajaProveedorInfoClimaticaFinca__isnull=True).__len__() == 0:
                raise ValueError(ERROR_FINCA_NO_TIENE_PROVEEDOR_HABILITADO, "La finca no tiene un proveedor habilitado")
            proveedor_finca = finca.proveedorinformacionclimaticafinca_set.get(
                fechaBajaProveedorInfoClimaticaFinca__isnull=True)
            proveedor = proveedor_finca.proveedorInformacionClimatica
            lista_tipo_medicion_climatica = []
            for tipo_medicion in proveedor.tipoMedicionClimatica.filter(habilitada=True):
                    lista_tipo_medicion_climatica.append(tipo_medicion)
            response.content = armar_response_list_content(lista_tipo_medicion_climatica)
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
def crear_configuracion_evento_personalizado(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if ((KEY_CONFIGURACION_MEDICION_INTERNA in datos)and(KEY_CONFIGURACION_MEDICION_EXTERNA in datos))\
                and(KEY_ID_USUARIO_FINCA in datos) and (KEY_NOMBRE_CONFIGURACION_EVENTO in datos) and \
                (KEY_NOTIFICACION_ACTIVADA in datos) and (KEY_CONFIGURACION_ACTIVADA in datos) and \
                (KEY_ID_SECTOR in datos):
            if  (datos[KEY_CONFIGURACION_MEDICION_INTERNA] == '' or datos[KEY_CONFIGURACION_MEDICION_EXTERNA] == ''):
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            sector = Sector.objects.get(idSector=datos[KEY_ID_SECTOR])
            usuario_finca = UsuarioFinca.objects.get(idUsuarioFinca=datos[KEY_ID_USUARIO_FINCA])
            configuracion_evento = ConfiguracionEventoPersonalizado(nombre=datos[KEY_NOMBRE_CONFIGURACION_EVENTO],
                                                                    notificacionActivada=datos[KEY_NOTIFICACION_ACTIVADA],
                                                                    activado=datos[KEY_CONFIGURACION_ACTIVADA],
                                                                    sector=sector, fechaHoraCreacion=datetime.now(),
                                                                    descripcion=datos[KEY_DESCRIPCION_CONFIGURACION_EVENTO],
                                                                fechaAltaConfiguracionEventoPersonalizado=datetime.now(),
                                                                    usuario_finca=usuario_finca
                                                                    )
            configuracion_evento.save()
            datos_configuracion_medicion_interna = datos[KEY_CONFIGURACION_MEDICION_INTERNA]
            for configuracion_interna in datos_configuracion_medicion_interna:
                tipo_medicion_interna = TipoMedicion.objects.get(
                    idTipoMedicion=configuracion_interna[KEY_ID_TIPO_MEDICION])
                medicion_fuente_interna = MedicionFuenteInterna(
                    valorMaximo=configuracion_interna[KEY_VALOR_MAXIMO],
                    valorMinimo=configuracion_interna[KEY_VALOR_MINIMO],
                    tipoMedicion=tipo_medicion_interna,
                    configuracionEventoPersonalizado=configuracion_evento)
                medicion_fuente_interna.save()
            datos_configuracion_medicion_externa = datos[KEY_CONFIGURACION_MEDICION_EXTERNA]
            for configuracion_externa in datos_configuracion_medicion_externa:
                tipo_medicion_externa = TipoMedicionClimatica.objects.get(
                    idTipoMedicionClimatica=configuracion_externa[KEY_ID_TIPO_MEDICION_CLIMATICA])
                medicion_estado_externo = MedicionEstadoExterno(
                    valorMaximo=configuracion_externa[KEY_VALOR_MAXIMO],
                    valorMinimo=configuracion_externa[KEY_VALOR_MINIMO],
                    tipoMedicion=tipo_medicion_externa,
                    configuracionEventoPersonalizado=configuracion_evento)
                medicion_estado_externo.save()
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
def modificar_configuracion_evento_personalizado(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if ((KEY_CONFIGURACION_MEDICION_INTERNA in datos)and(KEY_CONFIGURACION_MEDICION_EXTERNA in datos))\
                and(KEY_ID_USUARIO_FINCA in datos) and (KEY_NOMBRE_CONFIGURACION_EVENTO in datos) and \
                (KEY_NOTIFICACION_ACTIVADA in datos) and (KEY_CONFIGURACION_ACTIVADA in datos) and \
                (KEY_ID_SECTOR in datos) and (KEY_ID_CONFIGURACION_EVENTO_PERSONALIZADO in datos):
            if  (datos[KEY_CONFIGURACION_MEDICION_INTERNA] == '' and datos[KEY_CONFIGURACION_MEDICION_EXTERNA] == '')\
                    or (datos[KEY_ID_USUARIO_FINCA] == '') or (datos[KEY_NOMBRE_CONFIGURACION_EVENTO] == '')\
                    or (datos[KEY_NOTIFICACION_ACTIVADA] == '')\
                    or (datos[KEY_CONFIGURACION_ACTIVADA] == '') or (datos[KEY_ID_SECTOR] == '') or \
                    (datos[KEY_ID_CONFIGURACION_EVENTO_PERSONALIZADO] == ''):
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            sector = Sector.objects.get(idSector=datos[KEY_ID_SECTOR])
            usuario_finca = UsuarioFinca.objects.get(idUsuarioFinca=datos[KEY_ID_USUARIO_FINCA])
            configuracion_evento = ConfiguracionEventoPersonalizado.objects.get(
                idConfiguracion=datos[KEY_ID_CONFIGURACION_EVENTO_PERSONALIZADO])
            configuracion_evento.nombre=datos[KEY_NOMBRE_CONFIGURACION_EVENTO]
            configuracion_evento.notificacionActivada=datos[KEY_NOTIFICACION_ACTIVADA]
            configuracion_evento.activado=datos[KEY_CONFIGURACION_ACTIVADA]
            configuracion_evento.descripcion = datos[KEY_DESCRIPCION_CONFIGURACION_EVENTO]
            configuracion_evento.sector = sector
            configuracion_evento.medicionEventoList.all().delete()
            configuracion_evento.save()
            datos_configuracion_medicion_interna = datos[KEY_CONFIGURACION_MEDICION_INTERNA]
            for configuracion_interna in datos_configuracion_medicion_interna:
                tipo_medicion_interna = TipoMedicion.objects.get(
                    idTipoMedicion=configuracion_interna[KEY_ID_TIPO_MEDICION])
                medicion_fuente_interna = MedicionFuenteInterna(
                    valorMaximo=configuracion_interna[KEY_VALOR_MAXIMO],
                    valorMinimo=configuracion_interna[KEY_VALOR_MINIMO],
                    tipoMedicion=tipo_medicion_interna,
                    configuracionEventoPersonalizado=configuracion_evento)
                medicion_fuente_interna.save()
            datos_configuracion_medicion_externa = datos[KEY_CONFIGURACION_MEDICION_EXTERNA]
            for configuracion_externa in datos_configuracion_medicion_externa:
                tipo_medicion_externa = TipoMedicionClimatica.objects.get(
                    idTipoMedicionClimatica=configuracion_externa[KEY_ID_TIPO_MEDICION_CLIMATICA])
                medicion_estado_externo = MedicionEstadoExterno(
                    valorMaximo=configuracion_externa[KEY_VALOR_MAXIMO],
                    valorMinimo=configuracion_externa[KEY_VALOR_MINIMO],
                    tipoMedicion=tipo_medicion_externa,
                    configuracionEventoPersonalizado=configuracion_evento)
                medicion_estado_externo.save()
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
def desactivar_configuracion_evento_personalizado(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_ID_CONFIGURACION_EVENTO_PERSONALIZADO in datos):
            if  datos[KEY_ID_CONFIGURACION_EVENTO_PERSONALIZADO] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if ConfiguracionEventoPersonalizado.objects.filter(
                    idConfiguracion=datos[KEY_ID_CONFIGURACION_EVENTO_PERSONALIZADO]).__len__() == 0:
                raise ValueError(ERROR_CONFIGURACION_EVENTO_NO_ENCONTRADA,
                                 "No se encuentra una configuracion de evento con ese id")
            if ConfiguracionEventoPersonalizado.objects.filter(
                    idConfiguracion=datos[KEY_ID_CONFIGURACION_EVENTO_PERSONALIZADO], activado=True).__len__() == 0:
                raise ValueError(ERROR_CONFIGURACION_EVENTO_YA_DESACTIVADA,
                                 "No se puede desactivar la configuración de evento porque ya se encuentra desactivada")
            configuracion = ConfiguracionEventoPersonalizado.objects.get(
                    idConfiguracion=datos[KEY_ID_CONFIGURACION_EVENTO_PERSONALIZADO])
            configuracion.activado = False
            configuracion.save()
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
def activar_configuracion_evento_personalizado(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_ID_CONFIGURACION_EVENTO_PERSONALIZADO in datos):
            if  datos[KEY_ID_CONFIGURACION_EVENTO_PERSONALIZADO] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if ConfiguracionEventoPersonalizado.objects.filter(
                    idConfiguracion=datos[KEY_ID_CONFIGURACION_EVENTO_PERSONALIZADO]).__len__() == 0:
                raise ValueError(ERROR_CONFIGURACION_EVENTO_NO_ENCONTRADA,
                                 "No se encuentra una configuracion de evento con ese id")
            if ConfiguracionEventoPersonalizado.objects.filter(
                    idConfiguracion=datos[KEY_ID_CONFIGURACION_EVENTO_PERSONALIZADO], activado=True).__len__() == 1:
                raise ValueError(ERROR_CONFIGURACION_EVENTO_YA_ACTIVADA,
                                 "No se puede activar la configuración de evento porque ya se encuentra activada")
            configuracion = ConfiguracionEventoPersonalizado.objects.get(
                    idConfiguracion=datos[KEY_ID_CONFIGURACION_EVENTO_PERSONALIZADO])
            configuracion.activado = True
            configuracion.save()
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