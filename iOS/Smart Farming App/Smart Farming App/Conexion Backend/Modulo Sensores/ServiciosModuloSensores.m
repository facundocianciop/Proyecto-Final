//
//  ServiciosModuloSensores.m
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/24/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "ServiciosModuloSensores.h"

#pragma mark - operaciones

#define OPERATION_MOSTRAR_COMPONENTES_SENSOR_FINCA              @"mostrarComponentesSensorFinca"
#define OPERATION_MOSTRAR_COMPONENTES_SENSOR_FINCA_HABILITADOS  @"mostrarComponentesSensorFincaHabilitados"

#define OPERATION_MOSTRAR_TIPO_MEDICION                         @"mostrarTipoMedicion"
#define OPERATION_MOSTRAR_SENSORES_FINCA                        @"mostrarSensoresFinca"

@implementation ServiciosModuloSensores

+(void) mostrarComponentesSensorFinca:(SolicitudMostrarComponentesSensorFinca*)solicitudMostrarComponentesSensorFinca completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock {
    
    NSMutableDictionary *parametrosLlamada = [NSMutableDictionary new];
    if (solicitudMostrarComponentesSensorFinca) {
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudMostrarComponentesSensorFinca.idFinca] forKey:KEY_ID_FINCA];
    }
    
    [[HTTPConector instance] httpOperation:OPERATION_MOSTRAR_COMPONENTES_SENSOR_FINCA method:METHOD_POST withParameters:parametrosLlamada completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaMostrarComponentesSensorFinca *respuesta = [RespuestaMostrarComponentesSensorFinca new];
        
        NSDictionary *datosOperacion = [ServiciosModuloSensores armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        if (respuesta.resultado && datosOperacion) {
            
            @try {
                
                NSMutableArray *listaComponentesSensor = [NSMutableArray new];
                
                for (NSDictionary *datos in datosOperacion) {
                    
                    SFComponenteSensor *componenteSensor = [SFComponenteSensor new];
                    
                    if ([datos objectForKey:@"idComponenteSensor"] != [NSNull null]) {
                        componenteSensor.idComponenteSensor = [[datosOperacion objectForKey:@"idComponenteSensor"] longLongValue];
                    }
                    
                    if ([datos objectForKey:@"finca"] != [NSNull null]) {
                        componenteSensor.idFinca = [[datosOperacion objectForKey:@"finca"] longLongValue];
                    }
                    
                    if ([datos objectForKey:@"modelo"] != [NSNull null]) {
                        componenteSensor.modelo = [datosOperacion objectForKey:@"modelo"];
                    }
                    if ([datos objectForKey:@"descripcion"] != [NSNull null]) {
                        componenteSensor.descripcion = [datosOperacion objectForKey:@"descripcion"];
                    }
                    
                    if ([datos objectForKey:@"estado"] != [NSNull null]) {
                        componenteSensor.estadoComponenteSensor = [datosOperacion objectForKey:@"estado"];
                    }

                    if ([datos objectForKey:@"cantidadMaximaSensores"] != [NSNull null]) {
                        componenteSensor.cantidadMaximaSensores = [[datosOperacion objectForKey:@"cantidadMaximaSensores"] integerValue];
                    }
                    if ([datos objectForKey:@"cantidadSensoresAsignados"] != [NSNull null]) {
                        componenteSensor.cantidadSensoresAsignados = [[datosOperacion objectForKey:@"cantidadSensoresAsignados"] integerValue];
                    }
                    
                    [listaComponentesSensor addObject:componenteSensor];
                }
                
                respuesta.componentesSensor = listaComponentesSensor;
                
            } @catch (NSException *exception) {
                completionBlock(respuesta);
            }
        }
        completionBlock(respuesta);
        
    } failureBlock:^(NSError *error) {
        failureBlock([BaseServicios armarErrorServicio:error]);
    }];
    
}

+(void) mostrarComponentesSensorFincaHabilitados:(SolicitudMostrarComponentesSensorFincaHabilitados*)solicitudMostrarComponentesSensorFincaHabilitados completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock {
    
    NSMutableDictionary *parametrosLlamada = [NSMutableDictionary new];
    if (solicitudMostrarComponentesSensorFincaHabilitados) {
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudMostrarComponentesSensorFincaHabilitados.idFinca] forKey:KEY_ID_FINCA];
    }
    
    [[HTTPConector instance] httpOperation:OPERATION_MOSTRAR_COMPONENTES_SENSOR_FINCA_HABILITADOS method:METHOD_POST withParameters:parametrosLlamada completionBlock:^(NSDictionary *responseObject) {
        
         RespuestaMostrarComponentesSensorFincaHabilitados *respuesta = [RespuestaMostrarComponentesSensorFincaHabilitados new];
        
        NSDictionary *datosOperacion = [ServiciosModuloSensores armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        if (respuesta.resultado && datosOperacion) {
            
            @try {
                
                NSMutableArray *listaComponentesSensor = [NSMutableArray new];
                
                for (NSDictionary *datos in datosOperacion) {
                    
                    SFComponenteSensor *componenteSensor = [SFComponenteSensor new];
                    
                    if ([datos objectForKey:@"idComponenteSensor"] != [NSNull null]) {
                        componenteSensor.idComponenteSensor = [[datosOperacion objectForKey:@"idComponenteSensor"] longLongValue];
                    }
                    
                    if ([datos objectForKey:@"finca"] != [NSNull null]) {
                        componenteSensor.idFinca = [[datosOperacion objectForKey:@"finca"] longLongValue];
                    }
                    
                    if ([datos objectForKey:@"modelo"] != [NSNull null]) {
                        componenteSensor.modelo = [datosOperacion objectForKey:@"modelo"];
                    }
                    if ([datos objectForKey:@"descripcion"] != [NSNull null]) {
                        componenteSensor.descripcion = [datosOperacion objectForKey:@"descripcion"];
                    }
                    
                    if ([datos objectForKey:@"estado"] != [NSNull null]) {
                        componenteSensor.estadoComponenteSensor = [datosOperacion objectForKey:@"estado"];
                    }
                    
                    if ([datos objectForKey:@"cantidadMaximaSensores"] != [NSNull null]) {
                        componenteSensor.cantidadMaximaSensores = [[datosOperacion objectForKey:@"cantidadMaximaSensores"] integerValue];
                    }
                    if ([datos objectForKey:@"cantidadSensoresAsignados"] != [NSNull null]) {
                        componenteSensor.cantidadSensoresAsignados = [[datosOperacion objectForKey:@"cantidadSensoresAsignados"] integerValue];
                    }
                    
                    [listaComponentesSensor addObject:componenteSensor];
                }
                
                respuesta.componentesSensor = listaComponentesSensor;
                
            } @catch (NSException *exception) {
                completionBlock(respuesta);
            }
        }
        completionBlock(respuesta);
        
    } failureBlock:^(NSError *error) {
        failureBlock([BaseServicios armarErrorServicio:error]);
    }];
}

+(void) mostrarTipoMedicion:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock {
    
    [[HTTPConector instance] httpOperation:OPERATION_MOSTRAR_TIPO_MEDICION method:METHOD_GET withParameters:nil completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaMostrarTipoMedicion *respuesta = [RespuestaMostrarTipoMedicion new];
        
        NSDictionary *datosOperacion = [ServiciosModuloSensores armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        if (respuesta.resultado && datosOperacion) {
            
            @try {
                
                NSMutableArray *listaTiposMedicion = [NSMutableArray new];
                
                for (NSDictionary *datos in datosOperacion) {
                    
                    SFTipoMedicion *tipoMedicion = [SFTipoMedicion new];
                    
                    if ([datos objectForKey:@"idTipoMedicion"] != [NSNull null]) {
                        tipoMedicion.idTipoMedicion = [[datosOperacion objectForKey:@"idTipoMedicion"] longLongValue];
                    }
                    
                    if ([datos objectForKey:@"nombreTipoMedicion"] != [NSNull null]) {
                        tipoMedicion.nombreTipoMedicion = [datosOperacion objectForKey:@"nombreTipoMedicion"];
                    }
                    if ([datos objectForKey:@"unidadMedicion"] != [NSNull null]) {
                        tipoMedicion.unidadMedicion = [datosOperacion objectForKey:@"unidadMedicion"];
                    }
                    
                    if ([datos objectForKey:@"fechaAltaTipoMedicion"] != [NSNull null]) {
                        tipoMedicion.fechaAltaTipoMedicion = [SFUtils dateFromStringYYYYMMDD:datosOperacion[@"fechaAltaTipoMedicion"]];
                    }
                    if ([datos objectForKey:@"fechaBajaTipoMedicion"] != [NSNull null]) {
                        tipoMedicion.fechaBajaTipoMedicion = [SFUtils dateFromStringYYYYMMDD:datosOperacion[@"fechaBajaTipoMedicion"]];
                    }
                    
                    if ([datos objectForKey:@"habilitado"] != [NSNull null]) {
                        tipoMedicion.habilitado = [[datosOperacion objectForKey:@"habilitado"] boolValue];
                    }

                    [listaTiposMedicion addObject:tipoMedicion];
                }
                
                respuesta.tiposMedicion = listaTiposMedicion;
                
            } @catch (NSException *exception) {
                completionBlock(respuesta);
            }
        }
        completionBlock(respuesta);
        
    } failureBlock:^(NSError *error) {
        failureBlock([BaseServicios armarErrorServicio:error]);
    }];
}

+(void) mostrarSensoresFinca:(SolicitudMostrarSensoresFinca*)solicitudMostrarSensoresFinca completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock {
    
    NSMutableDictionary *parametrosLlamada = [NSMutableDictionary new];
    if (solicitudMostrarSensoresFinca) {
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudMostrarSensoresFinca.idFinca] forKey:KEY_ID_FINCA];
    }
    
    [[HTTPConector instance] httpOperation:OPERATION_MOSTRAR_SENSORES_FINCA method:METHOD_POST withParameters:parametrosLlamada completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaMostrarSensoresFinca *respuesta = [RespuestaMostrarSensoresFinca new];
        
        NSDictionary *datosOperacion = [ServiciosModuloSensores armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        if (respuesta.resultado && datosOperacion) {
            
            @try {
                
                NSMutableArray *listaSensores = [NSMutableArray new];
                
                for (NSDictionary *datos in datosOperacion) {
                    
                    SFSensor *sensor = [SFSensor new];
                    
                    if ([datos objectForKey:@"idSensor"] != [NSNull null]) {
                        sensor.idSensor = [[datosOperacion objectForKey:@"idSensor"] longLongValue];
                    }
                    
                    if ([datos objectForKey:@"tipoMedicion"] != [NSNull null]) {
                        sensor.nombreTipoMedicion = [datosOperacion objectForKey:@"tipoMedicion"];
                    }
                    if ([datos objectForKey:@"modelo"] != [NSNull null]) {
                        sensor.modelo = [datosOperacion objectForKey:@"modelo"];
                    }
                    
                    if ([datos objectForKey:@"fechaAltaSensor"] != [NSNull null]) {
                        sensor.fechaAltaSensor = [SFUtils dateFromStringYYYYMMDD:datosOperacion[@"fechaAltaSensor"]];
                    }
                    if ([datos objectForKey:@"fechaBajaSensor"] != [NSNull null]) {
                        sensor.fechaBajaSensor = [SFUtils dateFromStringYYYYMMDD:datosOperacion[@"fechaBajaSensor"]];
                    }
                    
                    if ([datos objectForKey:@"habilitado"] != [NSNull null]) {
                        sensor.habilitado = [[datosOperacion objectForKey:@"habilitado"] boolValue];
                    }
                    
                    [listaSensores addObject:sensor];
                }
                
                respuesta.sensoresFinca = listaSensores;
                
            } @catch (NSException *exception) {
                completionBlock(respuesta);
            }
        }
        completionBlock(respuesta);
        
    } failureBlock:^(NSError *error) {
        failureBlock([BaseServicios armarErrorServicio:error]);
    }];
    
}

@end
