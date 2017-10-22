# coding=utf-8
from json import dumps

from django.core.serializers.json import DjangoJSONEncoder

# Constantes Errores

ERROR_LOGIN_REQUERIDO = 'ERROR_LOGIN_REQUERIDO'
ERROR_LOGOUT_FALLIDO = 'ERROR_LOGOUT_FALLIDO'
ERROR_NO_TIENE_PERMISOS = 'ERROR_NO_TIENE_PERMISOS'
ERROR_DE_SISTEMA = 'ERROR_DE_SISTEMA'
ERROR_METODO_INCORRECTO = 'ERROR_METODO_INCORRECTO'
ERROR_DATOS_INCORRECTOS = 'ERROR_DATOS_INCORRECTOS'
ERROR_VALIDACION_DATOS = 'ERROR_VALIDACION_DATOS'
ERROR_DATOS_FALTANTES = 'ERROR_DATOS_FALTANTES'
ERROR_CREDENCIALES_INCORRECTAS = 'ERROR_CREDENCIALES_INCORRECTAS'

ERROR_USUARIO_YA_TIENE_ESE_ROL = 'ERROR_USUARIO_YA_TIENE_ESE_ROL'
ERROR_USUARIO_NO_ES_ENCARGADO = 'ERROR_USUARIO_NO_ES_ENCARGADO'
ERROR_USUARIO_NO_ENCONTRADO = 'ERROR_USUARIO_NO_ENCONTRADO'
ERROR_USUARIO_NO_ENCARGADO = 'ERROR_USUARIO_NO_ENCARGADO'
ERROR_USUARIO_EXISTENTE = 'ERROR_USUARIO_EXISTENTE'
ERROR_EMAIL_EXISTENTE = 'ERROR_EMAIL_EXISTENTE'
ERROR_USUARIO_FINCA_NO_ENCONTRADO = 'ERROR_USUARIO_FINCA_NO_ENCONTRADO'
ERROR_USUARIO_NO_HABILITADO_EN_FINCA = 'ERROR_USUARIO_NO_HABILITADO_EN_FINCA'
ERROR_USUARIO_YA_TIENE_ROL_EN_FINCA = 'ERROR_USUARIO_YA_TIENE_ROL_EN_FINCA'
ERROR_FINCA_YA_EXISTENTE = 'ERROR_FINCA_YA_EXISTENTE'
ERROR_PROVEEDOR_NO_ENCONTRADO = 'ERROR_PROVEEDOR_NO_ENCONTRADO'
ERROR_FINCA_NO_ENCONTRADA = 'ERROR_FINCA_NO_ENCONTRADA'
ERROR_FINCA_YA_APROBADA = 'ERROR_FINCA_YA_APROBADA'
ERROR_FINCA_YA_HABILITADA = 'ERROR_FINCA_YA_HABILITADA'
ERROR_FINCA_YA_DESAPROBADA = 'ERROR_FINCA_YA_DESAPROBADA'
ERROR_FINCA_YA_DESHABILITADA = 'ERROR_FINCA_YA_DESHABILITADA'
ERROR_SECTOR_SUPERA_TAMANIO_FINCA = 'ERROR_SECTOR_SUPERA_TAMANIO_FINCA'
ERROR_SECTORES_SUPERAN_TAMANIO_FINCA = 'ERROR_SECTORES_SUPERAN_TAMANIO_FINCA'
ERROR_SECTOR_YA_EXISTENTE = 'ERROR_SECTOR_YA_EXISTENTE'
ERROR_SECTOR_NO_ENCONTRADO = 'ERROR_SECTOR_NO_ENCONTRADO'
ERROR_SECTOR_NO_HABILITADO = 'ERROR_SECTOR_NO_HABILITADO'
ERROR_MECANISMO_RIEGO_FINCA_NO_EXISTE = 'ERROR_MECANISMO_RIEGO_FINCA_NO_EXISTE'
ERROR_MECANISMO_RIEGO_FINCA_NO_HABILITADO = 'ERROR_MECANISMO_RIEGO_FINCA_NO_HABILITADO'
ERROR_IP_YA_USADA = 'ERROR_IP_YA_USADA'
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
ERROR_COMPONENTE_SENSOR_YA_HABILITADO = 'ERROR_COMPONENTE_SENSOR_YA_HABILITADO'
ERROR_COMPONENTE_SENSOR_NO_ASIGNADO_A_SECTOR = 'ERROR_COMPONENTE_SENSOR_NO_ASIGNADO_A_SECTOR'
ERROR_SECTOR_YA_TIENE_COMPONENTE_HABILITADO = 'ERROR_SECTOR_YA_TIENE_COMPONENTE_HABILITADO'

ERROR_FINCA_NO_HABILITADA = 'ERROR_FINCA_NO_HABILITADA'
ERROR_FINCA_NO_TIENE_PROVEEDOR_HABILITADO = 'ERROR_FINCA_NO_TIENE_PROVEEDOR_HABILITADO'
ERROR_FRECUENCIA_MAXIMA_SUPERADA = 'ERROR_FRECUENCIA_MAXIMA_SUPERADA'
ERROR_NO_EXISTE_PROVEEDOR_FINCA = 'ERROR_NO_EXISTE_PROVEEDOR_FINCA'
ERROR_FINCA_TIENE_UN_PROVEEDOR_HABILITADO = 'ERROR_FINCA_TIENE_UN_PROVEEDOR_HABILITADO'

# Modulo configuracion riego
ERROR_EJECUCION_RIEGO = "ERROR_EJECUCION_RIEGO"

# Modulo reportes
ERROR_CONFIGURACION_EVENTO_NO_ENCONTRADA = 'ERROR_CONFIGURACION_EVENTO_NO_ENCONTRADA'
ERROR_CONFIGURACION_EVENTO_YA_DESACTIVADA = 'ERROR_CONFIGURACION_EVENTO_YA_DESACTIVADA'
ERROR_CONFIGURACION_EVENTO_YA_ACTIVADA = 'ERROR_CONFIGURACION_EVENTO_YA_ACTIVADA'
ERROR_HELADA_NO_CARGADA = 'ERROR_HELADA_NO_CARGADA'

# Detalle errores

DETALLE_ERROR_DESCONOCIDO = "Error desconocido"
DETALLE_ERROR_DATOS_INCOMPLETOS = "Faltan ingresar datos"
DETALLE_ERROR_DATOS_INCORRECTOS = "Datos incorrectos"
DETALLE_ERROR_SISTEMA = "Error procesando llamada"
DETALLE_ERROR_ENVIO_EMAIL = "Error enviando email"

# Modulo seguridad
DETALLE_ERROR_LOG_IN_FALLIDO = 'Usuario o contraseña incorrectos'
DETALLE_ERROR_LOG_OUT_FALLIDO = 'Log out fallo'
DETALLE_ERROR_TIPO_SESION_DATOS_FALTANTES = 'Faltan datos de tipo de sesion'

DETALLE_ERROR_NO_TIENE_PERMISOS = 'Usuario no tiene permisos para ejecutar esta operacion'

DETALLE_ERROR_REGISTRACION_USUARIO_EXISTENTE = 'Usuario ya existe en el sistema'
DETALLE_ERROR_REGISTRACION_USUARIO_FALTANTE = 'Falta ingresar usuario'
DETALLE_ERROR_REGISTRACION_USUARIO_INCORRECTO = 'Usuario incorrecto'
DETALLE_ERROR_REGISTRACION_CONTRASENIA_FALTANTE = 'Falta ingresar contrasena'
DETALLE_ERROR_REGISTRACION_NOMBRE_FALTANTE = 'Falta ingresar nombre'
DETALLE_ERROR_REGISTRACION_NOMBRE_INCORRECTO = 'Nombre incorrecto'
DETALLE_ERROR_REGISTRACION_APELLIDO_FALTANTE = 'Falta ingresar apellido'
DETALLE_ERROR_REGISTRACION_APELLIDO_INCORRECTO = 'Apellido incorrecto'
DETALLE_ERROR_REGISTRACION_DNI_FALTANTE = 'Falta ingresar dni'
DETALLE_ERROR_REGISTRACION_DNI_INCORRECTO = 'Formato dni ingresado es incorrecto'
DETALLE_ERROR_REGISTRACION_CUIT_FALTANTE = 'Falta ingresar CUIT'
DETALLE_ERROR_REGISTRACION_CUIT_INCORRECTO = 'Formato CUIT ingresado es incorrecto'
DETALLE_ERROR_REGISTRACION_DOMICILIO_FALTANTE = 'Falta ingresar domicilio'
DETALLE_ERROR_REGISTRACION_DOMICILIO_INCORRECTO = 'Formato domicilio ingresado es incorrecto'
DETALLE_ERROR_REGISTRACION_FECHA_NACIMIENTO_FALTANTE = 'Falta ingresar fecha de nacimiento'
DETALLE_ERROR_REGISTRACION_FECHA_NACIMIENTO_INCORRECTO = 'Formato de fecha de nacimiento ingresada es incorrecto'
DETALLE_ERROR_REGISTRACION_IMAGEN_FALTANTE = 'Falta ingresar imagen'
DETALLE_ERROR_REGISTRACION_IMAGEN_INCORRECTA = 'Formato imagen de ingresada es incorrecto'

DETALLE_ERROR_EMAIL_EXISTENTE = 'Ya existe un usuario con ese email'
DETALLE_ERROR_EMAIL_FALTANTE = 'Falta ingresar email'
DETALLE_ERROR_EMAIL_INCORRECTO = 'Formato email incorrecto'

DETALLE_ERROR_CONTRASENIA_INCORRECTA = 'Contraseña incorrecta'
DETALLE_ERROR_CONTRASENIA_FORMATO_INCORRECTO = 'Formato contraseña incorrecto: debe tener mas de 8 caracteres y' \
                                                    ' no puede ser solo numérica'

DETALLE_ERROR_CONTRASENIA_VIEJA_INCORRECTA = 'La contraseña actual ingresada es incorrecta'
DETALLE_ERROR_CAMBIAR_CONTRASENIA_VIEJA_FALTANTE = 'Falta ingresar contraseña actual'
DETALLE_ERROR_CAMBIAR_CONTRASENIA_NUEVA_FALTANTE = 'Falta ingresar contraseña nueva'

DETALLE_ERROR_CODIGO_VERIFICACION_FALTANTE = 'Falta ingresar codigo de verificacion'
DETALLE_ERROR_CODIGO_VERIFICACION_INCORRECTO = 'Codigo de verificacion incorrecto'

# Finca
DETALLE_ERROR_FINCA_DATOS_FALTANTES = "Falta ingresar datos de finca"

# Modulo configuracion riego
DETALLE_ERROR_EJECUION_RIEGO = "Ejecucion de riego fallo"
DETALLE_ERROR_DETENCION_RIEGO = "Detencion de riego fallo"

DETALLE_ERROR_MODIFICACION_CONFIGURACION_RIEGO = 'La configuracion de riego ya fue eliminada'
DETALLE_ERROR_CONFIGURACION_RIEGO_INCORRECTA = 'La configuracion de riego es incorrecta'
DETALLE_ERROR_RELACION_CONFIGURACION_RIEGO_CRITERIO = 'El criterio de riego no se corresponde con la configuracion'
DETALLE_ERROR_TIPO_CRITERIO_RIEGO_INCORRECTO = 'El tipo de criterio riego es incorrecto'
DETALLE_ERROR_TIPO_CRITERIO_RIEGO_INCORRECTO_MEDICION = "El criterio elegido no es por medicion"
DETALLE_ERROR_TIPO_CRITERIO_RIEGO_INCORRECTO_HORA = "El criterio elegido no es por hora"
DETALLE_ERROR_TIPO_CRITERIO_RIEGO_INCORRECTO_VOLUMEN = "El criterio elegido no es por volumen de agua"
DETALLE_ERROR_TIPO_CRITERIO_RIEGO_INICIAL_INCORRECTO = 'El tipo de criterio riego no es valido como criterio inicial'
DETALLE_ERROR_TIPO_CRITERIO_RIEGO_FINAL_INCORRECTO = 'El tipo de criterio riego no es valido como criterio final'
DETALLE_ERROR_CRITERIO_RIEGO_INEXISTENTE = 'El criterio de riego seleccionado no existe'
DETALLE_ERROR_CRITERIO_RIEGO_VALOR_MEDICION_INEXISTENTE = 'Falta ingresar valor de medicion'
DETALLE_ERROR_CRITERIO_RIEGO_TIPO_MEDICION_INEXISTENTE = 'Falta ingresar tipo de medicion'
DETALLE_ERROR_CRITERIO_RIEGO_HORA_INICIO_INEXISTENTE = 'Falta ingresar hora de inicio'
DETALLE_ERROR_CRITERIO_RIEGO_DIA_INICIO_INEXISTENTE = 'Falta ingresar dia de inicio'
DETALLE_ERROR_CRITERIO_RIEGO_VOLUMEN_INEXISTENTE = 'Falta ingresar volumen de agua'

DETALLE_ERROR_CONFIGURACION_RIEGO_AUTOMATICA_CRITERIO = 'A una configuracion de riego automatica no se le asignan' \
                                                        ' criterios'
DETALLE_ERROR_CONFIGURACION_RIEGO_CANTIDAD_MAX_CRITERIO_INICIAL = 'La cantidad maxima de criterios iniciales fue ' \
                                                                  'alcanzada'
DETALLE_ERROR_CONFIGURACION_RIEGO_CANTIDAD_MAX_CRITERIO_FINAL = 'La cantidad maxima de criterios finales fue alcanzada'


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
