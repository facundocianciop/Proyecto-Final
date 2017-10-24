//
//  BaseServicios.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 9/21/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "HTTPConector.h"

#import "ErrorServicioBase.h"
#import "SolicitudServicioBase.h"
#import "RespuestaServicioBase.h"

#import "SFUtils.h"

#pragma mark - Definicion de bloques

typedef void(^WorkBlock)(void);
typedef void(^FailureBlock)(ErrorServicioBase *error);
typedef void(^SuccessBlock)(RespuestaServicioBase *respuesta);

#pragma mark - Keys Diccionarios

// Sesion
#define PARAM_SESSION_ID        @"nro_sesion"
#define KEY_TIPO_SESION         @"idTipoSesion"

// Operacion
#define KEY_RESULTADO_OPERACION @"resultado"
#define KEY_DETALLE_OPERACION   @"detalle_operacion"
#define KEY_DATOS_OPERACION     @"datos_operacion"

// Roles
#define ROL_ENCARGADO           @"encargado"
#define ROL_STAKEHOLDER         @"stakeholder"

// Datos usuario
#define KEY_ID_USUARIO          @"idUsuario"
#define KEY_USUARIO             @"usuario"
#define KEY_KEY_USUARIO         @"KEY_USUARIO"
#define KEY_EMAIL               @"email"
#define KEY_KEY_EMAIL           @"KEY_EMAIL"
#define KEY_NOMBRE_USUARIO      @"nombre"
#define KEY_APELLIDO_USUARIO    @"apellido"

#define KEY_CONTRASENIA         @"contrasenia"
#define KEY_CONTRASENIA_VIEJA   @"contraseniaVieja"
#define KEY_CONTRASENIA_NUEVA   @"contraseniaNueva"
#define KEY_CODIGO_VERIFICACION @"codigoVerificacion"

#define KEY_DNI                 @"dni"
#define KEY_CUIT                @"cuit"
#define KEY_DOMICILIO           @"domicilio"
#define KEY_FECHA_NACIMIENTO    @"fechaNacimiento"
#define KEY_IMAGEN_USUARIO      @"imagenUsuario"

// Datos finca
#define KEY_ID_FINCA                @"idFinca"
#define KEY_NOMBRE_FINCA            @"nombreFinca"
#define KEY_NOMBRE_FINCA_RESPUESTA @"nombre"
#define KEY_DIRECCION_LEGAL         @"direccionLegal"
#define KEY_UBICACION               @"ubicacion"
#define KEY_TAMANIO                 @"tamanio"
#define KEY_LOGO                    @"logo"
#define KEY_ESTADO_FINCA            @"estadoFinca"
#define KEY_ID_USUARIO_FINCA        @"idUsuarioFinca"
#define KEY_NOMBRE_ROL              @"nombreRol"

// Mecanismo riego
#define KEY_NOMBRE_TIPO_MECANISMO               @"nombreTipoMecanismo"
#define KEY_ID_MECANISMO_RIEGO_FINCA            @"idMecanismoRiegoFinca"
#define KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR     @"idMecanismoRiegoFincaSector"
#define KEY_NOMBRE_PROVEEDOR                    @"nombreProveedor"
#define KEY_MECANISMO_RIEGO_CAUDAL              @"caudalMecanismoRiego"
#define KEY_MECANISMO_RIEGO_PRESION             @"presionMecanismoRiego"
#define KEY_MECANISMO_RIEGO_CAUDAL_RESPUESTA    @"caudal"
#define KEY_MECANISMO_RIEGO_PRESION_RESPUESTA   @"presion"

// Sector
#define KEY_NUMERO_SECTOR               @"numeroSector"
#define KEY_NOMBRE_SECTOR               @"nombreSector"
#define KEY_DESCRIPCION_SECTOR          @"descripcionSector"
#define KEY_SUPERFICIE_SECTOR           @"superficieSector"
#define KEY_ID_SECTOR                   @"idSector"

// Subtipo Cultivos
#define KEY_NOMBRE_SUBTIPO_CULTIVO  @"nombreSubtipoCultivo"

// Cultivo
#define KEY_NOMBRE_CULTIVO                  @"nombreCultivo"
#define KEY_DESCRIPCION_CULTIVO             @"descripcionCultivo"
#define KEY_ID_CULTIVO                      @"idCultivo"

#define KEY_NOMBRE_CULTIVO_SECTOR               @"nombre"
#define KEY_DESCRIPCION_CULTIVO_SECTOR          @"descripcion"
#define KEY_FECHA_PLANTACION_CULTIVO_SECTOR     @"fechaPlantacion"
#define KEY_FECHA_ELIMINACION_CULTIVO_SECTOR    @"fechaEliminacion"
#define KEY_TIPO_CULTIVO_SECTOR                 @"tipo"
#define KEY_SUBTIPO_CULTIVO_SECTOR              @"subtipo"
#define KEY_HABILITADO_CULTIVO_SECTOR           @"habilitado"

// Sensores
#define KEY_ID_TIPO_MEDICION    @"idTipoMedicion"
#define KEY_MODELO_SENSOR       @"modeloSensor"
#define KEY_ID_SENSOR           @"idSensor"

#define KEY_ID_COMPONENTE_SENSOR        @"idComponenteSensor"
#define KEY_MODELO_COMPONENTE           @"modeloComponente"
#define KEY_DESCRIPCION_COMPONENTE      @"descripcionComponente"
#define KEY_CANTIDAD_MAXIMA_SENSORES    @"cantidadMaximaSensores"
#define KEY_CANTIDAD_SENSORES_ASIGNADOS @"cantidadSensoresAsignados"

#define KEY_MODELO_COMPONENTE_SENSOR_RESPUESTA      @"modelo"
#define KEY_DESCRIPCION_COMPONENTE_SENSOR_RESPUESTA @"descripcion"
#define KEY_FINCA_COMPONENTE_SENSOR_RESPUESTA       @"finca"
#define KEY_ESTADO_COMPONENTE_SENSOR_RESPUESTA      @"estado"

// Configuracion riego
#define KEY_ID_CONFIGURACION_RIEGO              @"idConfiguracionRiego"
#define KEY_NOMBRE_CONFIGURACION_RIEGO          @"nombreConfiguracionRiego"
#define KEY_DESCRIPCION_CONFIGURACION_RIEGO     @"descripcionConfiguracionRiego"
#define KEY_DURACION_MAXIMA_CONFIGURACION_RIEGO @"duracionMaximaConfiguracionRiego"
#define KEY_ID_TIPO_CONFIGURACION_RIEGO         @"idTipoConfiguracionRiego"

#define KEY_ID_CRITERIO_RIEGO               @"idCriterioRiego"
#define KEY_NOMBRE_CRITERIO_RIEGO           @"nombreCriterioRiego"
#define KEY_DESCRIPCION_CRITERIO_RIEGO      @"descripcionCriterioRiego"
#define KEY_TIPO_CRITERIO_RIEGO             @"tipoCriterioRiego"  //TIPO_CONFIGURACION_RIEGO_PROGRAMADO/TIPO_CONFIGURACION_RIEGO_AUTOMATICO
#define KEY_VALOR_MEDICION_CRITERIO_RIEGO   @"valorMedicionCriterioRiego"
#define KEY_VOLUMEN_AGUA_CRITERIO_RIEGO     @"volumenAguaCriterioRiego"
#define KEY_HORA_INICIO_CRITERIO_RIEGO      @"horaInicioCriterioRiego"
#define KEY_DIA_INICIO_CRITERIO_RIEGO       @"diaInicioCriterioRiego"

// Obtencion informacion externa
#define KEY_PROVEEDOR_INFO_EXTERNA_NOMBRE_PROVEEDOR             @"nombreProveedor"
#define KEY_PROVEEDOR_INFO_EXTERNA_FRECUENCIA_MAXIMA_POSIBLE    @"frecuenciaMaximaPosible"
#define KEY_PROVEEDOR_INFO_EXTERNA_FRECUENCIA_ACTUAL            @"frecuenciaActual"
#define KEY_PROVEEDOR_INFO_EXTERNA_FECHA_ALTA_PROVEEDOR_FINCA   @"fechaAltaProveedorFinca"
#define KEY_PROVEEDOR_INFO_EXTERNA_URL_API                      @"urlApi"
#define KEY_PROVEEDOR_INFO_EXTERNA_LISTA_TIPO_MEDICION          @"listaTipoMedicion"

#define KEY_MEDICION_CLIMATICA_ID_TIPO_MEDICION_CLIMATICA            @"idTipoMedicionClimatica"
#define KEY_MEDICION_CLIMATICA_NOMBRE_TIPO_MEDICION_CLIMATICA        @"nombreTipoMedicionClimatica"
#define KEY_MEDICION_CLIMATICA_UNIDAD_MEDICION                       @"unidadMedicion"
#define KEY_MEDICION_CLIMATICA_FECHA_ALTA_TIPO_MEDICION_CLIMATICA    @"fechaAltaTipoMedicionClimatica"
#define KEY_MEDICION_CLIMATICA_FECHA_BAJA_TIPO_MEDICION_CLIMATICA    @"fechaBajaTipoMedicionClimatica"
#define KEY_MEDICION_CLIMATICA_HABILITADA                            @"habilitada"

// Mediciones
#define KEY_LISTA_MEDICIONES        @"listaMediciones"
#define KEY_VALOR_MEDICION_SENSOR   @"valorMedicion"

// Evento personalizado
#define KEY_ID_CONFIGURACION_EVENTO_PERSONALIZADO   @"idConfiguracionEvento"
#define KEY_CONFIGURACION_MEDICION_INTERNA          @"configuracionMedicionInterna"
#define KEY_CONFIGURACION_MEDICION_EXTERNA          @"configuracionMedicionExterna"
#define KEY_VALOR_MAXIMO                            @"valorMaximo"
#define KEY_VALOR_MINIMO                            @"valorMinimo"
#define KEY_ID_TIPO_MEDICION_CLIMATICA              @"idTipoMedicionClimatica"
#define KEY_NOMBRE_CONFIGURACION_EVENTO             @"nombreConfiguracionEvento"
#define KEY_NOTIFICACION_ACTIVADA                   @"notificacionActivada"
#define KEY_CONFIGURACION_ACTIVADA                  @"configuracionActivada"
#define KEY_DESCRIPCION_CONFIGURACION_EVENTO        @"descripcionConfiguracionEvento"

// Permisos
#define KEY_PERMISO_PUEDE_ASIGNAR_COMPONENTE_SENSOR                         @"puedeAsignarComponenteSensor"
#define KEY_PERMISO_PUEDE_ASIGNAR_CULTIVO                                   @"puedeAsignarCultivo"
#define KEY_PERMISO_PUEDE_ASIGNAR_MECRIEGO_A_FINCA                          @"puedeAsignarMecRiegoAFinca"
#define KEY_PERMISO_PUEDE_ASIGNAR_MECRIEGO_A_SECTOR                         @"puedeAsignarMecRiegoASector"
#define KEY_PERMISO_PUEDE_CONFIGURAR_OBTENCION_INFO_EXTERNA                 @"puedeConfigurarObtencionInfoExterna"
#define KEY_PERMISO_PUEDE_CREAR_COMPONENTE_SENSOR                           @"puedeCrearComponenteSensor"
#define KEY_PERMISO_PUEDE_CREAR_CONFIGURACION_RIEGO                         @"puedeCrearConfiguracionRiego"
#define KEY_PERMISO_PUEDE_CREAR_SECTOR                                      @"puedeCrearSector"
#define KEY_PERMISO_PUEDE_GENERAR_INFORME_CRUZADO_RIEGO_MEDICION            @"puedeGenerarInformeCruzadoRiegoMedicion"
#define KEY_PERMISO_PUEDE_GENERAR_INFORME_ESTADO_ACTUAL_SECTORES            @"puedeGenerarInformeEstadoActualSectores"
#define KEY_PERMISO_PUEDE_GENERAR_INFORME_ESTADO_HISTORICO_SECTORES_FINCA   @"puedeGenerarInformeEstadoHistoricoSectoresFinca"
#define KEY_PERMISO_PUEDE_GENERAR_INFORME_EVENTO_PERSONALIZADO              @"puedeGenerarInformeEventoPersonalizado"
#define KEY_PERMISO_PUEDE_GENERAR_INFORME_HELADAS_HISTORICO                 @"puedeGenerarInformeHeladasHistorico"
#define KEY_PERMISO_PUEDE_GENERAR_INFORME_RIEGO_EN_EJECUCION                @"puedeGenerarInformeRiegoEnEjecucion"
#define KEY_PERMISO_PUEDE_GENERAR_INFORME_RIEGO_POR_SECTORES_HISTORICO      @"puedeGenerarInformeRiegoPorSectoresHistorico"
#define KEY_PERMISO_PUEDE_GESTIONAR_COMPONENTE_SENSOR                       @"puedeGestionarComponenteSensor"
#define KEY_PERMISO_PUEDE_GESTIONAR_CULTIVO_SECTOR                          @"puedeGestionarCultivoSector"
#define KEY_PERMISO_PUEDE_GESTIONAR_EVENTO_PERSONALIZADO                    @"puedeGestionarEventoPersonalizado"
#define KEY_PERMISO_PUEDE_GESTIONAR_FINCA                                   @"puedeGestionarFinca"
#define KEY_PERMISO_PUEDE_GESTIONAR_SECTOR                                  @"puedeGestionarSector"
#define KEY_PERMISO_PUEDE_GESTIONAR_SENSORES                                @"puedeGestionarSensores"
#define KEY_PERMISO_PUEDE_GESTIONAR_USUARIOS_FINCA                          @"puedeGestionarUsuariosFinca"
#define KEY_PERMISO_PUEDE_INICIAR_O_DETENER_RIEGO_MANUALMENTE               @"puedeIniciarODetenerRiegoManualmente"
#define KEY_PERMISO_PUEDE_MODIFICAR_CONFIGURACION_RIEGO                     @"puedeModificarConfiguracionRiego"

@interface BaseServicios : NSObject

+(id)armarRespuestaServicio:(RespuestaServicioBase *)respuesta withResponseObject:(NSDictionary *)responseObject;
+(ErrorServicioBase*)armarErrorServicio:(NSError*)error;

@end
