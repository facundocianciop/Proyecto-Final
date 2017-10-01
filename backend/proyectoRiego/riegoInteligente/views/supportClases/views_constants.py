# Constantes Metodos

METHOD_PUT = 'PUT'
METHOD_POST = 'POST'
METHOD_GET = 'GET'
METHOD_DELETE = 'DELETE'


# Constantes Dictionary Keys

KEY_TIPO_SESION = 'tipoSesion'

KEY_RESULTADO_OPERACION = 'resultado'
KEY_DETALLE_OPERACION = 'detalle_operacion'

# Datos usuario
KEY_USUARIO = 'usuario'
KEY_EMAIL = 'email'

KEY_CONTRASENIA = 'contrasenia'
KEY_CONTRASENIA_VIEJA = 'contraseniaVieja'
KEY_CONTRASENIA_NUEVA = 'contraseniaNueva'
KEY_CODIGO_VERIFICACION = 'codigoVerificacion'

KEY_NOMBRE_USUARIO = 'nombre'
KEY_APELLIDO_USUARIO = 'apellido'

KEY_DNI = 'dni'
KEY_CUIT = 'cuit'
KEY_DOMICILIO = 'domicilio'
KEY_FECHA_NACIMIENTO = 'fechaNacimiento'
KEY_IMAGEN_USUARIO = 'imagenUsuario'

# Datos finca
KEY_NOMBRE_FINCA = 'nombreFinca'
KEY_ID_FINCA = 'idFinca'
KEY_DIRECCION_LEGAL = 'direccionLegal'
KEY_UBICACION = 'ubicacion'
KEY_TAMANIO = 'tamanio'
KEY_LOGO = 'logo'
KEY_ESTADO_FINCA = 'estadoFinca'
KEY_ID_USUARIO_FINCA = 'usuarioFincaId'
KEY_NOMBRE_ROL = 'nombreRol'
KEY_ID_MECANISMO_RIEGO_FINCA = 'idMecanismoRiegoFinca'
KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR = 'idMecanismoRiegoFincaSector'
KEY_NOMBRE_PROVEEDOR = 'nombreProveedor'
KEY_MECANISMO_RIEGO_CAUDAL = 'caudalMecanismoRiego'
KEY_MECANISMO_RIEGO_PRESION = 'presionMecanismoRiego'
KEY_ID_CONFIGURACION_RIEGO = 'idConfiguracionRiego'

# Sector
KEY_NUMERO_SECTOR = 'numeroSector'
KEY_NOMBRE_SECTOR = 'nombreSector'
KEY_DESCRIPCION_SECTOR = 'descripcionSector'
KEY_SUPERFICIE_SECTOR = 'superficieSector'
KEY_ID_SECTOR = 'idSector'

# Subtipo Cultivos
KEY_NOMBRE_SUBTIPO_CULTIVO = "nombreSubtipoCultivo"

# Cultivo
KEY_NOMBRE_CULTIVO = "nombreCultivo"
KEY_DESCRIPCION_CULTIVO = "descripcionCultivo"
KEY_FECHA_PLANTACION = "fechaPlantacion"
KEY_ID_CULTIVO = 'idCultivo'

# Roles
ROL_ENCARGADO = "encargado"
ROL_STAKEHOLDER = "stakeholder"

# Mecanismos
KEY_NOMBRE_TIPO_MECANISMO = 'nombreTipoMecanismo'

KEY_ID_TIPO_MEDICION = 'idTipoMedicion'
KEY_MODELO_SENSOR = 'modeloSensor'
KEY_ID_SENSOR = 'idSensor'


# Estados

ESTADO_ACTIVADO = 'activado'
ESTADO_DESACTIVADO = 'desactivado'
ESTADO_HABILITADO = 'habilitado'
ESTADO_DESHABILITADO = 'deshabilitado'
ESTADO_ELIMINADO = 'eliminado'
ESTADO_PENDIENTE_APROBACION = 'pendienteAprobacion'
ESTADO_NO_APROBADO = 'noAprobado'

ESTADO_EN_EJECUCION = 'en_ejecucion'
ESTADO_CANCELADO = 'cancelado'
ESTADO_PAUSADO = 'pausado'


# Detalle operaciones

DETALLE_OPERACION_VACIA = "no_hay_datos"

# Detalle operacion riego

DETALLE_RIEGO_EJECUCION_EN_PROCESO = "riego_ya_se_esta_ejecutando"
DETALLE_RIEGO_YA_PAUSADO = "riego_ya_esta_pausado"
DETALLE_RIEGO_INICIADO = "riego_iniciado_correctamente"
DETALLE_RIEGO_PAUSADO = "riego_pausado_correctamente"
DETALLE_RIEGO_REANUDADO = "riego_reanudado_correctamente"
DETALLE_RIEGO_CANCELADO = "riego_cancelado_correctamente"
DETALLE_RIEGO_NO_ACTIVO = "riego_no_hay_riego_activo"


# Tipos de criterio riego

TIPO_CRITERIO_RIEGO_MEDICION = "criterio_riego_medicion"
TIPO_CRITERIO_RIEGO_VOLUMEN_AGUA = "criterio_riego_volumen_agua"
TIPO_CRITERIO_RIEGO_HORA = "criterio_riego_hora"
