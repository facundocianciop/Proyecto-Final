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
