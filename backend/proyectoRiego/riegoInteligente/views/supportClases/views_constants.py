# coding=utf-8

# Constantes Metodos

METHOD_PUT = 'PUT'
METHOD_POST = 'POST'
METHOD_GET = 'GET'
METHOD_DELETE = 'DELETE'


# Constantes Dictionary Keys

KEY_TIPO_SESION = 'idTipoSesion'

KEY_RESULTADO_OPERACION = 'resultado'
KEY_DETALLE_OPERACION = 'detalle_operacion'
KEY_DATOS_OPERACION = 'datos_operacion'

# Roles
ROL_ENCARGADO = "encargado"
ROL_STAKEHOLDER = "stakeholder"

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
KEY_ID_USUARIO_FINCA = 'idUsuarioFinca'
KEY_NOMBRE_ROL = 'nombreRol'

# Mecanismo riego
KEY_NOMBRE_TIPO_MECANISMO = 'nombreTipoMecanismo'
KEY_ID_MECANISMO_RIEGO_FINCA = 'idMecanismoRiegoFinca'
KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR = 'idMecanismoRiegoFincaSector'
KEY_NOMBRE_PROVEEDOR = 'nombreProveedor'
KEY_MECANISMO_RIEGO_CAUDAL = 'caudalMecanismoRiego'
KEY_MECANISMO_RIEGO_PRESION = 'presionMecanismoRiego'

# Sector
KEY_NUMERO_SECTOR = 'numeroSector'
KEY_NOMBRE_SECTOR = 'nombreSector'
KEY_DESCRIPCION_SECTOR = 'descripcionSector'
KEY_SUPERFICIE_SECTOR = 'superficieSector'
KEY_ID_SECTOR = 'idSector'

# Subtipo Cultivos
KEY_NOMBRE_SUBTIPO_CULTIVO = "nombreSubtipoCultivo"

# Cultivo
KEY_NOMBRE_CULTIVO = 'nombreCultivo'
KEY_DESCRIPCION_CULTIVO = 'descripcionCultivo'
KEY_FECHA_PLANTACION = 'fechaPlantacion'
KEY_ID_CULTIVO = 'idCultivo'

# Sensores
KEY_ID_TIPO_MEDICION = 'idTipoMedicion'
KEY_MODELO_SENSOR = 'modeloSensor'
KEY_ID_SENSOR = 'idSensor'

KEY_ID_COMPONENTE_SENSOR = 'idComponenteSensor'
KEY_MODELO_COMPONENTE = "modeloComponente"
KEY_DESCRIPCION_COMPONENTE = "descripcionComponente"
KEY_CANTIDAD_MAXIMA_SENSORES = 'cantidadMaximaSensores'

# Configuracion riego
KEY_ID_CONFIGURACION_RIEGO = 'idConfiguracionRiego'
KEY_NOMBRE_CONFIGURACION_RIEGO = 'nombreConfiguracionRiego'
KEY_DESCRIPCION_CONFIGURACION_RIEGO = 'descripcionConfiguracionRiego'
KEY_DURACION_MAXIMA_CONFIGURACION_RIEGO = 'duracionMaximaConfiguracionRiego'
KEY_ID_TIPO_CONFIGURACION_RIEGO = 'idTipoConfiguracionRiego'

KEY_ID_CRITERIO_RIEGO = 'idCriterioRiego'
KEY_NOMBRE_CRITERIO_RIEGO = 'nombreCriterioRiego'
KEY_DESCRIPCION_CRITERIO_RIEGO = 'descripcionCriterioRiego'
KEY_TIPO_CRITERIO_RIEGO = 'tipoCriterioRiego'  # TIPO_CONFIGURACION_RIEGO_PROGRAMADO/TIPO_CONFIGURACION_RIEGO_AUTOMATICO
KEY_VALOR_MEDICION_CRITERIO_RIEGO = 'valorMedicionCriterioRiego'
KEY_VOLUMEN_AGUA_CRITERIO_RIEGO = 'volumenAguaCriterioRiego'
KEY_HORA_INICIO_CRITERIO_RIEGO = 'horaInicioCriterioRiego'
KEY_DIA_INICIO_CRITERIO_RIEGO = 'diaInicioCriterioRiego'

# Obtencion informacion externa
KEY_FRECUENCIA = 'frecuencia'

# Mediciones
KEY_LISTA_MEDICIONES = "listaMediciones"
KEY_VALOR_MEDICION_SENSOR = "valorMedicion"

# Evento personalizado
KEY_ID_CONFIGURACION_EVENTO_PERSONALIZADO = "idConfiguracionEvento"
KEY_CONFIGURACION_MEDICION_INTERNA = "configuracionMedicionInterna"
KEY_CONFIGURACION_MEDICION_EXTERNA = "configuracionMedicionExterna"
KEY_VALOR_MAXIMO = "valorMaximo"
KEY_VALOR_MINIMO = "valorMinimo"
KEY_ID_TIPO_MEDICION_CLIMATICA = "idTipoMedicionClimatica"
KEY_NOMBRE_CONFIGURACION_EVENTO = "nombreConfiguracionEvento"
KEY_NOTIFICACION_ACTIVADA = "notificacionActivada"
KEY_CONFIGURACION_ACTIVADA = "configuracionActivada"
KEY_DESCRIPCION_CONFIGURACION_EVENTO = "descripcionConfiguracionEvento"


# Detalle operaciones

DETALLE_OPERACION_VACIA = "No hay datos"

# Detalle operacion seguridad
DETALLE_REGISTRACION_USUARIO_CREADO_CORRECTAMENTE = "Usuario creado correctamente"
DETALLE_REGISTRACION_USUARIO_MODIFICADO_CORRECTAMENTE = "Usuario modificado correctamente"

DETALLE_CONTRASENIA_MODIFICADA_CORRECTAMENTE = 'Contraseña modificada correctamente'

DETALLE_RECUPERAR_CUENTA_EJECUTADA = "Recuperar cuenta se ejecuto correctamente"

# Detalle operacion riego
DETALLE_RIEGO_EJECUCION_EN_PROCESO = "El riego ya se esta ejecutando"
DETALLE_RIEGO_YA_PAUSADO = "El riego ya esta pausado"
DETALLE_RIEGO_INICIADO = "El riego fue iniciado correctamente"
DETALLE_RIEGO_PAUSADO = "El riego fue pausado correctamente"
DETALLE_RIEGO_REANUDADO = "El riego fue reanudado correctamente"
DETALLE_RIEGO_CANCELADO = "El riego fue cancelado correctamente"
DETALLE_RIEGO_NO_ACTIVO = "No hay riego activo"

# Detalle criterio riego
DETALLE_CRITERIO_RIEGO_CREADO = 'El criterio de riego fue creado'
DETALLE_CRITERIO_RIEGO_MODIFICADO = 'El criterio de riego fue modificado'
DETALLE_CRITERIO_RIEGO_ELIMINADO = 'El criterio de riego fue eliminado'


# Expresiones regulares

REGEX_CUIT = '^\d{2}\-\d{8}\-\d{1}$'


# Estados

ESTADO_ACTIVADO = 'activado'
ESTADO_DESACTIVADO = 'desactivado'
ESTADO_HABILITADO = 'habilitado'

ESTADO_EN_REPARACION = 'enReparacion'

ESTADO_DESHABILITADO = 'deshabilitado'
ESTADO_ELIMINADO = 'eliminado'

ESTADO_PENDIENTE_APROBACION = 'pendienteAprobacion'
ESTADO_NO_APROBADO = 'noAprobado'

ESTADO_EN_EJECUCION = 'en_ejecucion'
ESTADO_CANCELADO = 'cancelado'
ESTADO_PAUSADO = 'pausado'


# Tipos configuracion riego

TIPO_CONFIGURACION_RIEGO_PROGRAMADO = 'programado'
TIPO_CONFIGURACION_RIEGO_AUTOMATICO = 'automatico'

# Tipos de criterio riego

TIPO_CRITERIO_RIEGO_MEDICION = "criterio_riego_medicion"
TIPO_CRITERIO_RIEGO_VOLUMEN_AGUA = "criterio_riego_volumen_agua"
TIPO_CRITERIO_RIEGO_HORA = "criterio_riego_hora"
