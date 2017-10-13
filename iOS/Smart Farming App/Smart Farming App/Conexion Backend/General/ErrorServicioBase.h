//
//  ErrorServicioBase.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/11/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <Foundation/Foundation.h>

#pragma mark - Keys diccionario errores

#define KEY_ERROR_CODE          @"error_code"
#define KEY_ERROR_DESCRIPTION   @"error_description"

#pragma mark - Codigo errores

#define ERROR_LOGIN_REQUERIDO           @"ERROR_LOGIN_REQUERIDO"
#define ERROR_LOGOUT_FALLIDO            @"ERROR_LOGOUT_FALLIDO"
#define ERROR_NO_TIENE_PERMISOS         @"ERROR_NO_TIENE_PERMISOS"
#define ERROR_DE_SISTEMA                @"ERROR_DE_SISTEMA"
#define ERROR_METODO_INCORRECTO         @"ERROR_METODO_INCORRECTO"
#define ERROR_DATOS_INCORRECTOS         @"ERROR_DATOS_INCORRECTOS"
#define ERROR_VALIDACION_DATOS          @"ERROR_VALIDACION_DATOS"
#define ERROR_DATOS_FALTANTES           @"ERROR_DATOS_FALTANTES"
#define ERROR_CREDENCIALES_INCORRECTAS  @"ERROR_CREDENCIALES_INCORRECTAS"

#define ERROR_USUARIO_YA_TIENE_ESE_ROL              @"ERROR_USUARIO_YA_TIENE_ESE_ROL"
#define ERROR_USUARIO_NO_ENCONTRADO                 @"ERROR_USUARIO_NO_ENCONTRADO"
#define ERROR_USUARIO_NO_ENCARGADO                  @"ERROR_USUARIO_NO_ENCARGADO"
#define ERROR_USUARIO_EXISTENTE                     @"ERROR_USUARIO_EXISTENTE"
#define ERROR_EMAIL_EXISTENTE                       @"ERROR_EMAIL_EXISTENTE"
#define ERROR_USUARIO_FINCA_NO_ENCONTRADO           @"ERROR_USUARIO_FINCA_NO_ENCONTRADO"
#define ERROR_USUARIO_NO_HABILITADO_EN_FINCA        @"ERROR_USUARIO_NO_HABILITADO_EN_FINCA"
#define ERROR_FINCA_YA_EXISTENTE                    @"ERROR_FINCA_YA_EXISTENTE"
#define ERROR_PROVEEDOR_NO_ENCONTRADO               @"ERROR_PROVEEDOR_NO_ENCONTRADO"
#define ERROR_FINCA_NO_ENCONTRADA                   @"ERROR_FINCA_NO_ENCONTRADA"
#define ERROR_FINCA_YA_APROBADA                     @"ERROR_FINCA_YA_APROBADA"
#define ERROR_FINCA_YA_DESAPROBADA                  @"ERROR_FINCA_YA_DESAPROBADA"
#define ERROR_SECTOR_YA_EXISTENTE                   @"ERROR_SECTOR_YA_EXISTENTE"
#define ERROR_SECTOR_NO_ENCONTRADO                  @"ERROR_SECTOR_NO_ENCONTRADO"
#define ERROR_SECTOR_NO_HABILITADO                  @"ERROR_SECTOR_NO_HABILITADO"
#define ERROR_MECANISMO_RIEGO_FINCA_NO_HABILITADO   @"ERROR_MECANISMO_RIEGO_FINCA_NO_HABILITADO"
#define ERROR_MECANISMO_RIEGO_FINCA_YA_EXISTE       @"ERROR_MECANISMO_RIEGO_FINCA_YA_EXISTE"
#define ERROR_MECANISMO_RIEGO_FINCA_SECTOR_NO_HABILITADO @"ERROR_MECANISMO_RIEGO_FINCA_SECTOR_NO_HABILITADO"
#define ERROR_SECTOR_YA_TIENE_MECANISMO_HABILITADO  @"ERROR_SECTOR_YA_TIENE_MECANISMO_HABILITADO"
#define ERROR_MECANISMO_RIEGO_FINCA_SECTOR_NO_EXISTE    @"ERROR_MECANISMO_RIEGO_FINCA_SECTOR_NO_EXISTE"

#define ERROR_CULTIVO_NO_EXISTENTE              @"ERROR_CULTIVO_NO_EXISTENTE"
#define ERROR_CULTIVO_NO_HABILITADO             @"ERROR_CULTIVO_NO_HABILITADO"
#define ERROR_SUBTIPO_CULTIVO_NO_EXISTENTE      @"ERROR_SUBTIPO_CULTIVO_NO_EXISTENTE"
#define ERROR_SUBTIPO_CULTIVO_NO_HABILITADO     @"ERROR_SUBTIPO_CULTIVO_NO_HABILITADO"
#define ERROR_TIPO_CULTIVO_NO_HABILITADO        @"ERROR_TIPO_CULTIVO_NO_HABILITADO"
#define ERROR_SECTOR_YA_TIENE_CULTIVO_ASIGNADO  @"ERROR_SECTOR_YA_TIENE_CULTIVO_ASIGNADO"

#define ERROR_TIPO_MEDICION_NO_EXISTENTE    @"ERROR_TIPO_MEDICION_NO_EXISTENTE"
#define ERROR_TIPO_MEDICION_NO_HABILITADA   @"ERROR_TIPO_MEDICION_NO_HABILITADA"
#define ERROR_SENSOR_NO_EXISTENTE           @"ERROR_SENSOR_NO_EXISTENTE"

#define ERROR_SENSOR_NO_PERTENECE_A_FINCA               @"ERROR_SENSOR_NO_PERTENECE_A_FINCA"
#define ERROR_SENSOR_NO_HABILITADO                      @"ERROR_SENSOR_NO_HABILITADO"
#define ERROR_SENSOR_YA_ASIGNADO                        @"ERROR_SENSOR_YA_ASIGNADO"
#define ERROR_SENSOR_NO_ASIGNADO_A_COMPONENTE           @"ERROR_SENSOR_NO_ASIGNADO_A_COMPONENTE"
#define ERROR_COMPONENTE_NO_ACEPTA_MAS_SENSORES         @"ERROR_COMPONENTE_NO_ACEPTA_MAS_SENSORES"
#define ERROR_COMPONENTE_SENSOR_NO_EXISTENTE            @"ERROR_COMPONENTE_SENSOR_NO_EXISTENTE"
#define ERROR_COMPONENTE_SENSOR_NO_PERTENECE_A_FINCA    @"ERROR_COMPONENTE_SENSOR_NO_PERTENECE_A_FINCA"
#define ERROR_COMPONENTE_SENSOR_NO_HABILITADO           @"ERROR_COMPONENTE_SENSOR_NO_HABILITADO"
#define ERROR_COMPONENTE_SENSOR_YA_ASIGNADO             @"ERROR_COMPONENTE_SENSOR_YA_ASIGNADO"
#define ERROR_COMPONENTE_SENSOR_YA_HABILITADO           @"ERROR_COMPONENTE_SENSOR_YA_HABILITADO"
#define ERROR_COMPONENTE_SENSOR_NO_ASIGNADO_A_SECTOR    @"ERROR_COMPONENTE_SENSOR_NO_ASIGNADO_A_SECTOR"

#define ERROR_FINCA_NO_HABILITADA                   @"ERROR_FINCA_NO_HABILITADA"
#define ERROR_FINCA_NO_TIENE_PROVEEDOR_HABILITADO   @"ERROR_FINCA_NO_TIENE_PROVEEDOR_HABILITADO"
#define ERROR_FRECUENCIA_MAXIMA_SUPERADA            @"ERROR_FRECUENCIA_MAXIMA_SUPERADA"
#define ERROR_NO_EXISTE_PROVEEDOR_FINCA             @"ERROR_NO_EXISTE_PROVEEDOR_FINCA"
#define ERROR_FINCA_TIENE_UN_PROVEEDOR_HABILITADO   @"ERROR_FINCA_TIENE_UN_PROVEEDOR_HABILITADO"

// Modulo configuracion riego
#define ERROR_EJECUCION_RIEGO       @"ERROR_EJECUCION_RIEGO"

// Modulo reportes
#define ERROR_CONFIGURACION_EVENTO_NO_ENCONTRADA    @"ERROR_CONFIGURACION_EVENTO_NO_ENCONTRADA"
#define ERROR_CONFIGURACION_EVENTO_YA_DESACTIVADA   @"ERROR_CONFIGURACION_EVENTO_YA_DESACTIVADA"
#define ERROR_CONFIGURACION_EVENTO_YA_ACTIVADA      @"ERROR_CONFIGURACION_EVENTO_YA_ACTIVADA"


@interface ErrorServicioBase : NSError

@property (strong, nonatomic) NSString *codigoError;
@property (strong, nonatomic) NSString *detalleError;

@end
