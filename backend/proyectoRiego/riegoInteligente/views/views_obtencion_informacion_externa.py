from django.db import IntegrityError,transaction
from .supportClases.security_decorators import *

from ..models import *
from supportClases.views_util_functions import *
from supportClases.dto_obtencion_informacion_externa import *
@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
@manejar_errores()
def obtener_proveedor_finca(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_ID_FINCA) in datos:
            if datos[KEY_ID_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if Finca.objects.filter(idFinca=datos[KEY_ID_FINCA]).__len__() != 1:
                raise ValueError(ERROR_FINCA_NO_ENCONTRADA, "No existe la finca ingresada")
            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
            if finca.proveedorinformacionclimaticafinca_set.filter(
                fechaBajaProveedorInfoClimaticaFinca__isnull=True).__len__() == 0:
                raise ValueError(ERROR_FINCA_NO_TIENE_PROVEEDOR_HABILITADO,
                                 "La finca no tiene actualmente un proveedor configurado")
            proveedor_finca = finca.proveedorinformacionclimaticafinca_set.get(
                fechaBajaProveedorInfoClimaticaFinca__isnull=True)
            proveedor = proveedor_finca.proveedorInformacionClimatica
            lista_tipo_medicion = proveedor.tipoMedicionClimatica.all()
            lista_tipo_medicion_json = []
            for tipo_medicion in lista_tipo_medicion:
                lista_tipo_medicion_json.append(tipo_medicion.as_json())
            dto_proveedor_finca = DtoProveedorFinca(nombre_proveedor=proveedor.nombreProveedor,
                                                    fecha_alta_proveedor_finca
                                                    =proveedor_finca.fechaAltaProveedorInfoClimaticaFinca,
                                                    lista_tipo_medicion=lista_tipo_medicion_json,
                                                    url_api=proveedor.urlAPI,
                                                    frecuencia_maxima_posible=proveedor.frecuenciaMaxPosible,
                                                    frecuencia_actual=proveedor_finca.frecuencia)
            dto_proveedor_finca.lista_tipo_medicion = lista_tipo_medicion_json
            response.content = armar_response_content(dto_proveedor_finca)
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
@permisos_rol_requeridos([PERMISO_PUEDEGESTIONARFINCA])
def modificar_proveedor_finca(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_NOMBRE_PROVEEDOR in datos) and (KEY_ID_FINCA in datos) and (KEY_FRECUENCIA in datos):
            if datos[KEY_NOMBRE_PROVEEDOR] == '' or datos[KEY_ID_FINCA] == '' or datos[KEY_FRECUENCIA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if ProveedorInformacionClimatica.objects.filter(nombreProveedor=datos[KEY_NOMBRE_PROVEEDOR]).__len__() == 0:
                raise ValueError(ERROR_PROVEEDOR_NO_ENCONTRADO, "No se encuentra al proveedor con ese id.")

            proveedorSeleccionado = ProveedorInformacionClimatica.objects.get(nombreProveedor=datos[KEY_NOMBRE_PROVEEDOR])
            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
            proveedorInformacionClimaticaFinca = ProveedorInformacionClimaticaFinca.objects.get(
                    proveedorInformacionClimatica=proveedorSeleccionado, finca=finca,
                fechaBajaProveedorInfoClimaticaFinca__isnull=True)
            if int(datos[KEY_FRECUENCIA]) < proveedorSeleccionado.frecuenciaMaxPosible:
                raise ValueError(ERROR_FRECUENCIA_MAXIMA_SUPERADA, "No se puede colocar esa frecuencia, ya que es mayor a la permitida por el proveedor.")
            proveedorInformacionClimaticaFinca.frecuencia = datos[KEY_FRECUENCIA]
            proveedorInformacionClimaticaFinca.save()
            response.content = armar_response_content(None)
            response.status_code = 200
            return response
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
    except ValueError as err:
            return build_bad_request_error(response, err.args[0], err.args[1])
    except (IntegrityError, TypeError, KeyError):
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
@manejar_errores()
@permisos_rol_requeridos([PERMISO_PUEDEGESTIONARFINCA])
def deshabilitar_proveedor_finca(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_NOMBRE_PROVEEDOR and KEY_ID_FINCA) in datos:
            if datos[KEY_NOMBRE_PROVEEDOR] == '' or datos[KEY_ID_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if ProveedorInformacionClimatica.objects.filter(nombreProveedor=datos[KEY_NOMBRE_PROVEEDOR]).__len__() == 1:
                proveedorSeleccionado = ProveedorInformacionClimatica.objects.get(nombreProveedor=datos[KEY_NOMBRE_PROVEEDOR])
                finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
                if ProveedorInformacionClimaticaFinca.objects.filter(
                    proveedorInformacionClimatica=proveedorSeleccionado, finca=finca,
                    fechaBajaProveedorInfoClimaticaFinca__isnull=True).__len__() == 0:
                    raise ValueError(ERROR_NO_EXISTE_PROVEEDOR_FINCA, "No existe una relacion habilitada con ese proveedor")
                proveedorInformacionClimaticaFinca = ProveedorInformacionClimaticaFinca.objects.get(
                    proveedorInformacionClimatica=proveedorSeleccionado, finca=finca,
                    fechaBajaProveedorInfoClimaticaFinca__isnull=True)
                proveedorInformacionClimaticaFinca.fechaBajaProveedorInfoClimaticaFinca = datetime.now(pytz.utc)
                proveedorInformacionClimaticaFinca.save()
                response.content=armar_response_content(None)
                response.status_code = 200
                return response
            else:
                raise ValueError(ERROR_PROVEEDOR_NO_ENCONTRADO, "No se encontro el proveedor seleccionado")
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
    except ValueError as err:
            return build_bad_request_error(response, err.args[0], err.args[1])
    except (IntegrityError, TypeError, KeyError):
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
@manejar_errores()
@permisos_rol_requeridos([PERMISO_PUEDEGESTIONARFINCA])
def cambiar_proveedor_finca(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_NOMBRE_PROVEEDOR in datos)and(KEY_ID_FINCA in datos) and (KEY_FRECUENCIA in datos):
            if datos[KEY_NOMBRE_PROVEEDOR] == '' or datos[KEY_ID_FINCA] == '' or datos[KEY_FRECUENCIA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if Finca.objects.filter(idFinca=datos[KEY_ID_FINCA]).__len__ == 0:
                raise ValueError(ERROR_FINCA_NO_ENCONTRADA, "No se encuentra a la finca ingresada")
            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
            proveedor_finca_a_eliminar = finca.proveedorinformacionclimaticafinca_set.get(
                fechaBajaProveedorInfoClimaticaFinca__isnull=True)
            proveedor_finca_a_eliminar.fechaBajaProveedorInfoClimaticaFinca = datetime.now(pytz.utc)
            proveedor_finca_a_eliminar.save()
            if ProveedorInformacionClimatica.objects.filter(nombreProveedor=datos[KEY_NOMBRE_PROVEEDOR]).__len__() == 1:
                proveedorSeleccionado = ProveedorInformacionClimatica.objects.get(nombreProveedor=datos[KEY_NOMBRE_PROVEEDOR])
                if int(datos[KEY_FRECUENCIA]) < proveedorSeleccionado.frecuenciaMaxPosible:
                    # si la frecuencia de actualizacion es mayor a la permitida por el proveedor se retorna un error
                    raise ValueError(ERROR_FRECUENCIA_MAXIMA_SUPERADA,
                                     "No se puede colocar esa frecuencia, ya que es mayor a la permitida por el proveedor")
                proveedorInformacionClimaticaFinca = ProveedorInformacionClimaticaFinca(
                    frecuencia=datos[KEY_FRECUENCIA],
                    proveedorInformacionClimatica=proveedorSeleccionado, finca=finca,
                    fechaAltaProveedorInfoClimaticaFinca=datetime.now(pytz.utc))
                proveedorInformacionClimaticaFinca.save()
                response.content=armar_response_content(None)
                response.status_code = 200
                return response
            else:
                raise ValueError(ERROR_PROVEEDOR_NO_ENCONTRADO, "No se encontro el proveedor seleccionado")
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
    except ValueError as err:
            return build_bad_request_error(response, err.args[0], err.args[1])
    except (IntegrityError, TypeError, KeyError):
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")
