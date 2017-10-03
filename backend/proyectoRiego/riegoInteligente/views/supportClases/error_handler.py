from json import dumps

from django.core.serializers.json import DjangoJSONEncoder

# Constantes Errores

ERROR_LOGIN_REQUERIDO = 'ERROR_LOGIN_REQUERIDO'
ERROR_LOGOUT_FALLIDO = 'ERROR_LOGOUT_FALLIDO'

ERROR_DE_SISTEMA = 'ERROR_DE_SISTEMA'
ERROR_METODO_INCORRECTO = 'ERROR_METODO_INCORRECTO'
ERROR_DATOS_INCORRECTOS = 'ERROR_DATOS_INCORRECTOS'
ERROR_DATOS_FALTANTES = 'ERROR_DATOS_FALTANTES'
ERROR_CREDENCIALES_INCORRECTAS = 'ERROR_CREDENCIALES_INCORRECTAS'

ERROR_USUARIO_YA_TIENE_ESE_ROL = 'ERROR_USUARIO_YA_TIENE_ESE_ROL'
ERROR_USUARIO_NO_ENCONTRADO = 'ERROR_USUARIO_NO_ENCONTRADO'
ERROR_USUARIO_NO_ENCARGADO = 'ERROR_USUARIO_NO_ENCARGADO'
ERROR_USUARIO_EXISTENTE = 'ERROR_USUARIO_EXISTENTE'
ERROR_FINCA_YA_EXISTENTE = 'ERROR_FINCA_YA_EXISTENTE'
ERROR_PROVEEDOR_NO_ENCONTRADO = 'ERROR_PROVEEDOR_NO_ENCONTRADO'
ERROR_FINCA_NO_ENCONTRADA = 'ERROR_FINCA_NO_ENCONTRADA'
ERROR_FINCA_YA_APROBADA = 'ERROR_FINCA_YA_APROBADA'
ERROR_FINCA_YA_DESAPROBADA = 'ERROR_FINCA_YA_DESAPROBADA'
ERROR_SECTOR_YA_EXISTENTE = 'ERROR_SECTOR_YA_EXISTENTE'
ERROR_SECTOR_NO_ENCONTRADO = 'ERROR_SECTOR_NO_ENCONTRADO'
ERROR_SECTOR_NO_HABILITADO = 'ERROR_SECTOR_NO_HABILITADO'
ERROR_MECANISMO_RIEGO_FINCA_NO_HABILITADO = 'ERROR_MECANISMO_RIEGO_FINCA_NO_HABILITADO'
ERROR_MECANISMO_RIEGO_FINCA_YA_EXISTE = 'ERROR_MECANISMO_RIEGO_FINCA_YA_EXISTE'
ERROR_MECANISMO_RIEGO_FINCA_SECTOR_NO_HABILITADO = 'ERROR_MECANISMO_RIEGO_FINCA_SECTOR_NO_HABILITADO'
ERROR_SECTOR_YA_TIENE_MECANISMO_HABILITADO = 'ERROR_SECTOR_YA_TIENE_MECANISMO_HABILITADO'
ERROR_MECANISMO_RIEGO_FINCA_SECTOR_NO_EXISTE = 'ERROR_MECANISMO_RIEGO_FINCA_SECTOR_NO_EXISTE'

ERROR_CULTIVO_NO_EXISTENTE = 'ERROR_CULTIVO_NO_EXISTENTE'
ERROR_CULTIVO_NO_HABILITADO = 'ERROR_CULTIVO_NO_HABILITADO'
ERROR_SUBTIPO_CULTIVO_NO_EXISTENTE = "ERROR_SUBTIPO_CULTIVO_NO_EXISTENTE"
ERROR_SUBTIPO_CULTIVO_NO_HABILITADO = "ERROR_SUBTIPO_CULTIVO_NO_HABILITADO"
ERROR_TIPO_CULTIVO_NO_HABILITADO = "ERROR_TIPO_CULTIVO_NO_HABILITADO"
ERROR_SECTOR_YA_TIENE_CULTIVO_ASIGNADO = 'ERROR_SECTOR_YA_TIENE_CULTIVO_ASIGNADO'

ERROR_TIPO_MEDICION_NO_EXISTENTE = 'ERROR_TIPO_MEDICION_NO_EXISTENTE'
ERROR_TIPO_MEDICION_NO_HABILITADA = 'ERROR_TIPO_MEDICION_NO_HABILITADA'
ERROR_SENSOR_NO_EXISTENTE = 'ERROR_SENSOR_NO_EXISTENTE'

ERROR_SENSOR_NO_PERTENECE_A_FINCA = 'ERROR_SENSOR_NO_PERTENECE_A_FINCA'
ERROR_SENSOR_NO_HABILITADO = 'ERROR_SENSOR_NO_HABILITADO'
ERROR_SENSOR_YA_ASIGNADO = 'ERROR_SENSOR_YA_ASIGNADO'
ERROR_SENSOR_NO_ASIGNADO_A_COMPONENTE = 'ERROR_SENSOR_NO_ASIGNADO_A_COMPONENTE'
ERROR_COMPONENTE_NO_ACEPTA_MAS_SENSORES = 'ERROR_COMPONENTE_NO_ACEPTA_MAS_SENSORES'
ERROR_COMPONENTE_SENSOR_NO_EXISTENTE = 'ERROR_COMPONENTE_SENSOR_NO_EXISTENTE'
ERROR_COMPONENTE_SENSOR_NO_PERTENECE_A_FINCA = 'ERROR_COMPONENTE_SENSOR_NO_PERTENECE_A_FINCA'
ERROR_COMPONENTE_SENSOR_NO_HABILITADO = 'ERROR_COMPONENTE_SENSOR_NO_HABILITADO'
ERROR_COMPONENTE_SENSOR_YA_ASIGNADO = 'ERROR_COMPONENTE_SENSOR_YA_ASIGNADO'
ERROR_COMPONENTE_SENSOR_NO_ASIGNADO = 'ERROR_COMPONENTE_SENSOR_NO_ASIGNADO'
ERROR_COMPONENTE_SENSOR_YA_HABILITADO = 'ERROR_COMPONENTE_SENSOR_YA_HABILITADO'


ERROR_FINCA_NO_TIENE_PROVEEDOR_HABILITADO = 'ERROR_FINCA_NO_TIENE_PROVEEDOR_HABILITADO'
ERROR_FRECUENCIA_MAXIMA_SUPERADA = 'ERROR_FRECUENCIA_MAXIMA_SUPERADA'
ERROR_NO_EXISTE_PROVEEDOR_FINCA = 'ERROR_NO_EXISTE_PROVEEDOR_FINCA'
ERROR_FINCA_TIENE_UN_PROVEEDOR_HABILITADO = 'ERROR_FINCA_TIENE_UN_PROVEEDOR_HABILITADO'

# Modulo configuracion riego
ERROR_EJECUCION_RIEGO = "ERROR_EJECUCION_RIEGO"


# Detalle errores

DETALLE_ERROR_DESCONOCIDO = "error_desconocido"
DETALLE_ERROR_DATOS_INCOMPLETOS = "faltan_ingresar_datos"
DETALLE_ERROR_DATOS_INCORRECTOS = "datos_incorrectos"
DETALLE_ERROR_SISTEMA = "error_procesando_llamada"

# Modulo seguridad
DETALLE_ERROR_LOG_OUT_FALLIDO = 'log_out_fallo'

# Modulo configuracion riego
DETALLE_ERROR_EJECUION_RIEGO = "fallo_ejecucion_riego"
DETALLE_ERROR_DETENCION_RIEGO = "fallo_detencion_riego"

DETALLE_ERROR_MODIFICACION_CONFIGURACION_RIEGO = 'configuracion_riego_ya_fue_eliminada'
DETALLE_ERROR_TIPO_CRITERIO_RIEGO_INCORRECTO = 'tipo_criterio_riego_incorrecto'
DETALLE_ERROR_TIPO_CRITERIO_RIEGO_INICIAL_INCORRECTO = 'tipo_criterio_riego_no_valido_como_criterio_inicial'
DETALLE_ERROR_TIPO_CRITERIO_RIEGO_FINAL_INCORRECTO = 'tipo_criterio_riego_no_valido_como_criterio_final'



# Constantes Keys

KEY_ERROR_CODE = 'error_code'
KEY_ERROR_DESCRIPTION = 'error_description'


# Metodos

def build_error(response, error_code, error_descripcion):
    content = {KEY_ERROR_DESCRIPTION: error_descripcion, KEY_ERROR_CODE: error_code}
    response.content = dumps(content, cls=DjangoJSONEncoder)

    return response


def build_bad_request_error(response, error_code, error_descripcion):
    response.status_code = 400
    return build_error(response, error_code, error_descripcion)


def build_unauthorized_error(response, error_code, error_descripcion):
    response.status_code = 401

    return build_error(response, error_code, error_descripcion)


def build_method_not_allowed_error(response, error_code, error_descripcion):
    response.status_code = 405

    return build_error(response, error_code, error_descripcion)


def build_internal_server_error(response, error_code, error_descripcion):
    response.status_code = 500

    return build_error(response, error_code, error_descripcion)
