//
//  ServiciosModuloRiego.m
//  Smart Farming App
//
//  Created by Facundo Palma on 10/13/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "ServiciosModuloRiego.h"

#define OPERATION_OBTENER_RIEGO_ENEJECUCION_MECANISMO_RIEGO_FINCA_SECTOR        @"obtenerRiegoEnEjecucionMecanismoRiegoFincaSector"
#define OPERATION_INICIAR_RIEGO_MANUALMENTE                                     @"iniciarRiegoManualmente"
#define OPERATION_PAUSAR_RIEGO_MANUALMENTE                                      @"pausarRiegoManualmente"
#define OPERATION_CANCELAR_RIEGO_MANUALMENTE                                    @"cancelarRiegoManualmente"

#define OPERATION_OBTENER_CONFIGURACIONES_RIEGO_MECANISMO_RIEGO_FINCA_SECTOR    @"obtenerConfiguracionesRiegoMecanismoRiegoFincaSector"
#define OPERATION_OBTENER_CRITERIOS_INICIALES_CONFIGURACION_RIEGO_MECANISMO_RIEGO_FINCA_SECTOR @"obtenerCriteriosInicialesConfiguracionRiegoMecanismoRiegoFincaSector"
#define OPERATION_OBTENER_CRITERIOS_FINALES_CONFIGURACION_RIEGO_MECANISMO_RIEGO_FINCA_SECTOR   @"obtenerCriteriosFinalesConfiguracionRiegoMecanismoRiegoFincaSector"

@implementation ServiciosModuloRiego

+(void) obtenerRiegoEnEjecucionMecanismoRiegoFincaSector:(SolicitudObtenerRiegoEnEjecucionMecanismoRiegoFincaSector*)solicitudObtenerRiegoEnEjecucionMecanismoRiegoFincaSector completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock{
    
    NSMutableDictionary *parametrosLlamada = [NSMutableDictionary new];
    if (solicitudObtenerRiegoEnEjecucionMecanismoRiegoFincaSector) {
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudObtenerRiegoEnEjecucionMecanismoRiegoFincaSector.idFinca] forKey:KEY_ID_FINCA];
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudObtenerRiegoEnEjecucionMecanismoRiegoFincaSector.idMecanismoRiegoFincaSector] forKey:KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR];
    }
    
    [[HTTPConector instance] httpOperation:OPERATION_OBTENER_RIEGO_ENEJECUCION_MECANISMO_RIEGO_FINCA_SECTOR method:METHOD_POST withParameters:parametrosLlamada completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaObtenerRiegoEnEjecucionMecanismoRiegoFincaSector *respuesta = [RespuestaObtenerRiegoEnEjecucionMecanismoRiegoFincaSector new];
        
        NSDictionary *datosOperacion = [ServiciosModuloRiego armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        if (respuesta.resultado && datosOperacion) {
            
            @try {
                
                SFEjecucionRiego *ejecucionRiego = [SFEjecucionRiego new];
                
                if ([datosOperacion objectForKey:@"mecanismoRiegoFincaSector"] != [NSNull null]) {
                    ejecucionRiego.idMecanismoRiegoFincaSector = [[datosOperacion objectForKey:@"mecanismoRiegoFincaSector"] longLongValue];
                }
                if ([datosOperacion objectForKey:@"configuracion_riego"] != [NSNull null]) {
                    ejecucionRiego.idConfiguracionRiego = [[datosOperacion objectForKey:@"configuracion_riego"] longLongValue];
                }
                
                if ([datosOperacion objectForKey:@"estado_ejecucion_riego"] != [NSNull null]) {
                    ejecucionRiego.nombreEstadoEjecucionRiego = [datosOperacion objectForKey:@"estado_ejecucion_riego"];
                }
                if ([datosOperacion objectForKey:@"detalle"] != [NSNull null]) {
                    ejecucionRiego.detalle = [datosOperacion objectForKey:@"detalle"];
                }
                
                if ([datosOperacion objectForKey:@"cantidadAguaUtilizadaLitros"] != [NSNull null]) {
                    ejecucionRiego.cantidadAguaUtilizadaLitros = [[datosOperacion objectForKey:@"cantidadAguaUtilizadaLitros"] floatValue];
                }
                
                if ([datosOperacion objectForKey:@"duracionActualMinutos"] != [NSNull null]) {
                    ejecucionRiego.duracionActualMinutos = [[datosOperacion objectForKey:@"duracionActualMinutos"] floatValue];
                }
                if ([datosOperacion objectForKey:@"duracionActualSegundos"] != [NSNull null]) {
                    ejecucionRiego.duracionActualSegundos = [[datosOperacion objectForKey:@"duracionActualSegundos"] floatValue];
                }
                
                if ([datosOperacion objectForKey:@"fechaHoraFinalizacion"]!= [NSNull null]) {
                    ejecucionRiego.fechaHoraFinalizacion = [SFUtils dateFromStringYYYYMMDDWithTime:datosOperacion[@"fechaHoraFinalizacion"]];
                }
                if ([datosOperacion objectForKey:@"fechaHoraFinalProgramada"]!= [NSNull null]) {
                    ejecucionRiego.fechaHoraFinalProgramada = [SFUtils dateFromStringYYYYMMDDWithTime:datosOperacion[@"fechaHoraFinalProgramada"]];
                }
                
                if ([datosOperacion objectForKey:@"fechaHoraInicio"]!= [NSNull null]) {
                    ejecucionRiego.fechaHoraInicio = [SFUtils dateFromStringYYYYMMDDWithTime:datosOperacion[@"fechaHoraInicio"]];
                }
                if ([datosOperacion objectForKey:@"fechaHoraInicioProgramada"]!= [NSNull null]) {
                    ejecucionRiego.fechaHoraInicioProgramada = [SFUtils dateFromStringYYYYMMDDWithTime:datosOperacion[@"fechaHoraInicioProgramada"]];
                }
         
                respuesta.ejecucionRiego = ejecucionRiego;
                
            } @catch (NSException *exception) {
                completionBlock(respuesta);
            }
        }
        completionBlock(respuesta);
        
    } failureBlock:^(NSError *error) {
        failureBlock([BaseServicios armarErrorServicio:error]);
    }];
}

+(void) iniciarRiegoManualmente:(SolicitudIniciarRiegoManualmente*)solicitudIniciarRiegoManualmente completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock{
    
    NSMutableDictionary *parametrosLlamada = [NSMutableDictionary new];
    if (solicitudIniciarRiegoManualmente) {
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudIniciarRiegoManualmente.idFinca] forKey:KEY_ID_FINCA];
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudIniciarRiegoManualmente.idMecanismoRiegoFincaSector] forKey:KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR];
    }
    
    [[HTTPConector instance] httpOperation:OPERATION_INICIAR_RIEGO_MANUALMENTE method:METHOD_POST withParameters:parametrosLlamada completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaIniciarRiegoManualmente *respuesta = [RespuestaIniciarRiegoManualmente new];
        
        NSDictionary *datosOperacion = [ServiciosModuloRiego armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        if (respuesta.resultado && datosOperacion) {
            
            @try {
                
                SFEjecucionRiego *ejecucionRiego = [SFEjecucionRiego new];
                
                if ([datosOperacion objectForKey:@"mecanismoRiegoFincaSector"] != [NSNull null]) {
                    ejecucionRiego.idMecanismoRiegoFincaSector = [[datosOperacion objectForKey:@"mecanismoRiegoFincaSector"] longLongValue];
                }
                if ([datosOperacion objectForKey:@"configuracion_riego"] != [NSNull null]) {
                    ejecucionRiego.idConfiguracionRiego = [[datosOperacion objectForKey:@"configuracion_riego"] longLongValue];
                }
                
                if ([datosOperacion objectForKey:@"estado_ejecucion_riego"] != [NSNull null]) {
                    ejecucionRiego.nombreEstadoEjecucionRiego = [datosOperacion objectForKey:@"estado_ejecucion_riego"];
                }
                if ([datosOperacion objectForKey:@"detalle"] != [NSNull null]) {
                    ejecucionRiego.detalle = [datosOperacion objectForKey:@"detalle"];
                }
                
                if ([datosOperacion objectForKey:@"cantidadAguaUtilizadaLitros"] != [NSNull null]) {
                    ejecucionRiego.cantidadAguaUtilizadaLitros = [[datosOperacion objectForKey:@"cantidadAguaUtilizadaLitros"] floatValue];
                }
                
                if ([datosOperacion objectForKey:@"duracionActualMinutos"] != [NSNull null]) {
                    ejecucionRiego.duracionActualMinutos = [[datosOperacion objectForKey:@"duracionActualMinutos"] floatValue];
                }
                if ([datosOperacion objectForKey:@"duracionActualSegundos"] != [NSNull null]) {
                    ejecucionRiego.duracionActualSegundos = [[datosOperacion objectForKey:@"duracionActualSegundos"] floatValue];
                }
                
                if ([datosOperacion objectForKey:@"fechaHoraFinalizacion"]!= [NSNull null]) {
                    ejecucionRiego.fechaHoraFinalizacion = [SFUtils dateFromStringYYYYMMDDWithTime:datosOperacion[@"fechaHoraFinalizacion"]];
                }
                if ([datosOperacion objectForKey:@"fechaHoraFinalProgramada"]!= [NSNull null]) {
                    ejecucionRiego.fechaHoraFinalProgramada = [SFUtils dateFromStringYYYYMMDDWithTime:datosOperacion[@"fechaHoraFinalProgramada"]];
                }
                
                if ([datosOperacion objectForKey:@"fechaHoraInicio"]!= [NSNull null]) {
                    ejecucionRiego.fechaHoraInicio = [SFUtils dateFromStringYYYYMMDDWithTime:datosOperacion[@"fechaHoraInicio"]];
                }
                if ([datosOperacion objectForKey:@"fechaHoraInicioProgramada"]!= [NSNull null]) {
                    ejecucionRiego.fechaHoraInicioProgramada = [SFUtils dateFromStringYYYYMMDDWithTime:datosOperacion[@"fechaHoraInicioProgramada"]];
                }
                
                respuesta.ejecucionRiego = ejecucionRiego;
                
            } @catch (NSException *exception) {
                completionBlock(respuesta);
            }
        }
        completionBlock(respuesta);
        
    } failureBlock:^(NSError *error) {
        failureBlock([BaseServicios armarErrorServicio:error]);
    }];
}

+(void) pausarRiegoManualmente:(SolicitudPausarRiegoManualmente*)solicitudPausarRiegoManualmente completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock{
    
    NSMutableDictionary *parametrosLlamada = [NSMutableDictionary new];
    if (solicitudPausarRiegoManualmente) {
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudPausarRiegoManualmente.idFinca] forKey:KEY_ID_FINCA];
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudPausarRiegoManualmente.idMecanismoRiegoFincaSector] forKey:KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR];
    }
    
    [[HTTPConector instance] httpOperation:OPERATION_PAUSAR_RIEGO_MANUALMENTE method:METHOD_POST withParameters:parametrosLlamada completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaPausarRiegoManualmente *respuesta = [RespuestaPausarRiegoManualmente new];
        
        NSDictionary *datosOperacion = [ServiciosModuloRiego armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        if (respuesta.resultado && datosOperacion) {
            
            @try {
                
                SFEjecucionRiego *ejecucionRiego = [SFEjecucionRiego new];
                
                if ([datosOperacion objectForKey:@"mecanismoRiegoFincaSector"] != [NSNull null]) {
                    ejecucionRiego.idMecanismoRiegoFincaSector = [[datosOperacion objectForKey:@"mecanismoRiegoFincaSector"] longLongValue];
                }
                if ([datosOperacion objectForKey:@"configuracion_riego"] != [NSNull null]) {
                    ejecucionRiego.idConfiguracionRiego = [[datosOperacion objectForKey:@"configuracion_riego"] longLongValue];
                }
                
                if ([datosOperacion objectForKey:@"estado_ejecucion_riego"] != [NSNull null]) {
                    ejecucionRiego.nombreEstadoEjecucionRiego = [datosOperacion objectForKey:@"estado_ejecucion_riego"];
                }
                if ([datosOperacion objectForKey:@"detalle"] != [NSNull null]) {
                    ejecucionRiego.detalle = [datosOperacion objectForKey:@"detalle"];
                }
                
                if ([datosOperacion objectForKey:@"cantidadAguaUtilizadaLitros"] != [NSNull null]) {
                    ejecucionRiego.cantidadAguaUtilizadaLitros = [[datosOperacion objectForKey:@"cantidadAguaUtilizadaLitros"] floatValue];
                }
                
                if ([datosOperacion objectForKey:@"duracionActualMinutos"] != [NSNull null]) {
                    ejecucionRiego.duracionActualMinutos = [[datosOperacion objectForKey:@"duracionActualMinutos"] floatValue];
                }
                if ([datosOperacion objectForKey:@"duracionActualSegundos"] != [NSNull null]) {
                    ejecucionRiego.duracionActualSegundos = [[datosOperacion objectForKey:@"duracionActualSegundos"] floatValue];
                }
                
                if ([datosOperacion objectForKey:@"fechaHoraFinalizacion"]!= [NSNull null]) {
                    ejecucionRiego.fechaHoraFinalizacion = [SFUtils dateFromStringYYYYMMDDWithTime:datosOperacion[@"fechaHoraFinalizacion"]];
                }
                if ([datosOperacion objectForKey:@"fechaHoraFinalProgramada"]!= [NSNull null]) {
                    ejecucionRiego.fechaHoraFinalProgramada = [SFUtils dateFromStringYYYYMMDDWithTime:datosOperacion[@"fechaHoraFinalProgramada"]];
                }
                
                if ([datosOperacion objectForKey:@"fechaHoraInicio"]!= [NSNull null]) {
                    ejecucionRiego.fechaHoraInicio = [SFUtils dateFromStringYYYYMMDDWithTime:datosOperacion[@"fechaHoraInicio"]];
                }
                if ([datosOperacion objectForKey:@"fechaHoraInicioProgramada"]!= [NSNull null]) {
                    ejecucionRiego.fechaHoraInicioProgramada = [SFUtils dateFromStringYYYYMMDDWithTime:datosOperacion[@"fechaHoraInicioProgramada"]];
                }
                
                respuesta.ejecucionRiego = ejecucionRiego;
                
            } @catch (NSException *exception) {
                completionBlock(respuesta);
            }
        }
        completionBlock(respuesta);
        
    } failureBlock:^(NSError *error) {
        failureBlock([BaseServicios armarErrorServicio:error]);
    }];
}

+(void) cancelarRiegoManualmente:(SolicitudCancelarRiegoManualmente*)solicitudCancelarRiegoManualmente completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock{
    
    NSMutableDictionary *parametrosLlamada = [NSMutableDictionary new];
    if (solicitudCancelarRiegoManualmente) {
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudCancelarRiegoManualmente.idFinca] forKey:KEY_ID_FINCA];
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudCancelarRiegoManualmente.idMecanismoRiegoFincaSector] forKey:KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR];
    }
    
    [[HTTPConector instance] httpOperation:OPERATION_CANCELAR_RIEGO_MANUALMENTE method:METHOD_POST withParameters:parametrosLlamada completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaCancelarRiegoManualmente *respuesta = [RespuestaCancelarRiegoManualmente new];
        
        NSDictionary *datosOperacion = [ServiciosModuloRiego armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        if (respuesta.resultado && datosOperacion) {
            
            @try {
                
                SFEjecucionRiego *ejecucionRiego = [SFEjecucionRiego new];
                
                if ([datosOperacion objectForKey:@"mecanismoRiegoFincaSector"] != [NSNull null]) {
                    ejecucionRiego.idMecanismoRiegoFincaSector = [[datosOperacion objectForKey:@"mecanismoRiegoFincaSector"] longLongValue];
                }
                if ([datosOperacion objectForKey:@"configuracion_riego"] != [NSNull null]) {
                    ejecucionRiego.idConfiguracionRiego = [[datosOperacion objectForKey:@"configuracion_riego"] longLongValue];
                }
                
                if ([datosOperacion objectForKey:@"estado_ejecucion_riego"] != [NSNull null]) {
                    ejecucionRiego.nombreEstadoEjecucionRiego = [datosOperacion objectForKey:@"estado_ejecucion_riego"];
                }
                if ([datosOperacion objectForKey:@"detalle"] != [NSNull null]) {
                    ejecucionRiego.detalle = [datosOperacion objectForKey:@"detalle"];
                }
                
                if ([datosOperacion objectForKey:@"cantidadAguaUtilizadaLitros"] != [NSNull null]) {
                    ejecucionRiego.cantidadAguaUtilizadaLitros = [[datosOperacion objectForKey:@"cantidadAguaUtilizadaLitros"] floatValue];
                }
                
                if ([datosOperacion objectForKey:@"duracionActualMinutos"] != [NSNull null]) {
                    ejecucionRiego.duracionActualMinutos = [[datosOperacion objectForKey:@"duracionActualMinutos"] floatValue];
                }
                if ([datosOperacion objectForKey:@"duracionActualSegundos"] != [NSNull null]) {
                    ejecucionRiego.duracionActualSegundos = [[datosOperacion objectForKey:@"duracionActualSegundos"] floatValue];
                }
                
                if ([datosOperacion objectForKey:@"fechaHoraFinalizacion"]!= [NSNull null]) {
                    ejecucionRiego.fechaHoraFinalizacion = [SFUtils dateFromStringYYYYMMDDWithTime:datosOperacion[@"fechaHoraFinalizacion"]];
                }
                if ([datosOperacion objectForKey:@"fechaHoraFinalProgramada"]!= [NSNull null]) {
                    ejecucionRiego.fechaHoraFinalProgramada = [SFUtils dateFromStringYYYYMMDDWithTime:datosOperacion[@"fechaHoraFinalProgramada"]];
                }
                
                if ([datosOperacion objectForKey:@"fechaHoraInicio"]!= [NSNull null]) {
                    ejecucionRiego.fechaHoraInicio = [SFUtils dateFromStringYYYYMMDDWithTime:datosOperacion[@"fechaHoraInicio"]];
                }
                if ([datosOperacion objectForKey:@"fechaHoraInicioProgramada"]!= [NSNull null]) {
                    ejecucionRiego.fechaHoraInicioProgramada = [SFUtils dateFromStringYYYYMMDDWithTime:datosOperacion[@"fechaHoraInicioProgramada"]];
                }
                
                respuesta.ejecucionRiego = ejecucionRiego;
                
            } @catch (NSException *exception) {
                completionBlock(respuesta);
            }
        }
        completionBlock(respuesta);
        
    } failureBlock:^(NSError *error) {
        failureBlock([BaseServicios armarErrorServicio:error]);
    }];
}

+(void) obtenerConfiguracionesRiegoMecanismoRiegoFincaSector:(SolicitudObtenerConfiguracionesRiegoMecanismoRiegoFincaSector*)solicitudObtenerConfiguracionesRiegoMecanismoRiegoFincaSector completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock{
    
    NSMutableDictionary *parametrosLlamada = [NSMutableDictionary new];
    if (solicitudObtenerConfiguracionesRiegoMecanismoRiegoFincaSector) {
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudObtenerConfiguracionesRiegoMecanismoRiegoFincaSector.idFinca] forKey:KEY_ID_FINCA];
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudObtenerConfiguracionesRiegoMecanismoRiegoFincaSector.idMecanismoRiegoFincaSector] forKey:KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR];
    }
    
    [[HTTPConector instance] httpOperation:OPERATION_OBTENER_CONFIGURACIONES_RIEGO_MECANISMO_RIEGO_FINCA_SECTOR method:METHOD_POST withParameters:parametrosLlamada completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaObtenerConfiguracionesRiegoMecanismoRiegoFincaSector *respuesta = [RespuestaObtenerConfiguracionesRiegoMecanismoRiegoFincaSector new];
        
        NSDictionary *datosOperacion = [ServiciosModuloRiego armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        if (respuesta.resultado && datosOperacion) {
            
            @try {
                
                NSMutableArray *listaConfiguracionesRiego = [NSMutableArray new];
                
                for (NSDictionary *datos in datosOperacion) {
                    
                    SFConfiguracionRiego *configuracionRiego = [SFConfiguracionRiego new];
                    
                    if ([datos objectForKey:@"idConfiguracionRiego"] != [NSNull null]) {
                        configuracionRiego.idConfiguracionRiego = [[datos objectForKey:@"idConfiguracionRiego"] longLongValue];
                    }
                    if ([datos objectForKey:@"mecanismoRiegoFincaSector"] != [NSNull null]) {
                        configuracionRiego.idMecanismoRiegoFincaSector = [[datos objectForKey:@"mecanismoRiegoFincaSector"] longLongValue];
                    }
                    
                    if ([datos objectForKey:@"nombre"] != [NSNull null]) {
                        configuracionRiego.nombreConfiguracionRiego = [datos objectForKey:@"nombre"];
                    }
                    if ([datos objectForKey:@"descripcion"] != [NSNull null]) {
                        configuracionRiego.descripcionConfiguracionRiego = [datos objectForKey:@"descripcion"];
                    }
                    
                    if ([datos objectForKey:@"duracionMaxima"] != [NSNull null]) {
                        configuracionRiego.duracionMaxima = [[datos objectForKey:@"duracionMaxima"] floatValue];
                    }
                    
                    if ([datos objectForKey:@"fechaCreacion"]!= [NSNull null]) {
                        configuracionRiego.fechaCreacion = [SFUtils dateFromStringYYYYMMDD:datos[@"fechaCreacion"]];
                    }
                    if ([datos objectForKey:@"fechaFinalizacion"]!= [NSNull null]) {
                        configuracionRiego.fechaFinalizacion = [SFUtils dateFromStringYYYYMMDD:datos[@"fechaFinalizacion"]];
                    }
                
                    if ([datos objectForKey:@"tipoConfiguracionRiego"] != [NSNull null]) {
                        configuracionRiego.nombreTipoConfiguracionRiego = [datos objectForKey:@"tipoConfiguracionRiego"];
                    }
                    if ([datos objectForKey:@"estado_configuracion"] != [NSNull null]) {
                        configuracionRiego.nombreEstadoConfiguracionRiego = [datos objectForKey:@"estado_configuracion"];
                    }
                    
                    if ([datos objectForKey:@"fechaHoraInicio"]!= [NSNull null]) {
                        configuracionRiego.fechaHoraInicio = [SFUtils dateFromStringYYYYMMDD:datos[@"fechaHoraInicio"]];
                    }
                    if ([datos objectForKey:@"fechaHoraInicioProgramada"]!= [NSNull null]) {
                        configuracionRiego.fechaHoraInicioProgramada = [SFUtils dateFromStringYYYYMMDD:datos[@"fechaHoraInicioProgramada"]];
                    }
                    
                    [listaConfiguracionesRiego addObject:configuracionRiego];
                }
                
                respuesta.configuracionesRiego = listaConfiguracionesRiego;

            } @catch (NSException *exception) {
                completionBlock(respuesta);
            }
        }
        completionBlock(respuesta);
        
    } failureBlock:^(NSError *error) {
        failureBlock([BaseServicios armarErrorServicio:error]);
    }];
}

+(void) obtenerCriteriosInicialesConfiguracionRiegoMecanismoRiegoFincaSector:(SolicitudObtenerCriteriosInicialesConfiguracionRiegoMecanismoRiegoFincaSector*)solicitudObtenerCriteriosInicialesConfiguracionRiegoMecanismoRiegoFincaSector completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock{
    
    NSMutableDictionary *parametrosLlamada = [NSMutableDictionary new];
    if (solicitudObtenerCriteriosInicialesConfiguracionRiegoMecanismoRiegoFincaSector) {
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudObtenerCriteriosInicialesConfiguracionRiegoMecanismoRiegoFincaSector.idFinca] forKey:KEY_ID_FINCA];
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudObtenerCriteriosInicialesConfiguracionRiegoMecanismoRiegoFincaSector.idMecanismoRiegoFincaSector] forKey:KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR];
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudObtenerCriteriosInicialesConfiguracionRiegoMecanismoRiegoFincaSector.idConfiguracionRiego] forKey:KEY_ID_CONFIGURACION_RIEGO];
    }
    
    [[HTTPConector instance] httpOperation:OPERATION_OBTENER_CRITERIOS_INICIALES_CONFIGURACION_RIEGO_MECANISMO_RIEGO_FINCA_SECTOR method:METHOD_POST withParameters:parametrosLlamada completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaObtenerCriteriosInicialesConfiguracionRiegoMecanismoRiegoFincaSector *respuesta = [RespuestaObtenerCriteriosInicialesConfiguracionRiegoMecanismoRiegoFincaSector new];
        
        NSDictionary *datosOperacion = [ServiciosModuloRiego armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        if (respuesta.resultado && datosOperacion) {
            
            @try {
                
                NSMutableArray *listaCritetiosRiego = [NSMutableArray new];
                
                for (NSDictionary *datos in datosOperacion) {
                    
                    NSString *nombreTipoCriterioRiego = @"";
                    
                    if ([datos objectForKey:@"tipo_criterio_riego"] != [NSNull null]) {
                        nombreTipoCriterioRiego = [datos objectForKey:@"tipo_criterio_riego"];
                    }
                    
                    if ([nombreTipoCriterioRiego isEqualToString:TIPO_CRITERIO_RIEGO_MEDICION]) {
                        SFCriterioConfiguracionRiegoMedicion *criterioConfiguracion = [SFCriterioConfiguracionRiegoMedicion new];
                        
                        criterioConfiguracion.nombreTipoCriterioRiego = nombreTipoCriterioRiego;
                        
                        if ([datos objectForKey:@"id_criterio_riego"] != [NSNull null]) {
                            criterioConfiguracion.idCriterioRiego = [[datos objectForKey:@"id_criterio_riego"] longLongValue];
                        }
                        
                        if ([datos objectForKey:@"nombre"] != [NSNull null]) {
                            criterioConfiguracion.nombreCriterioRiego = [datos objectForKey:@"nombre"];
                        }
                        if ([datos objectForKey:@"descripcion"] != [NSNull null]) {
                            criterioConfiguracion.descripcionCriterioRiego = [datos objectForKey:@"descripcion"];
                        }
                        
                        if ([datos objectForKey:@"fechaCreacionCriterio"]!= [NSNull null]) {
                            criterioConfiguracion.fechaCreacionCriterio = [SFUtils dateFromStringYYYYMMDD:datos[@"fechaCreacionCriterio"]];
                        }
                        
                        // Valores especificos del tipo de criterio
                        
                        if ([datos objectForKey:@"unidadMedicion"] != [NSNull null]) {
                            criterioConfiguracion.unidadMedicion = [datos objectForKey:@"unidadMedicion"];
                        }
                        if ([datos objectForKey:@"tipoMedicion"] != [NSNull null]) {
                            criterioConfiguracion.nombreTipoMedicion = [datos objectForKey:@"tipoMedicion"];
                        }
                        
                        if ([datos objectForKey:@"operador"] != [NSNull null]) {
                            criterioConfiguracion.operador = [datos objectForKey:@"operador"];
                        }
                        if ([datos objectForKey:@"valor"] != [NSNull null]) {
                            criterioConfiguracion.valor = [[datos objectForKey:@"valor"] floatValue];
                        }
                        
                        [listaCritetiosRiego addObject:criterioConfiguracion];
                    }
                    else if ([nombreTipoCriterioRiego isEqualToString:TIPO_CRITERIO_RIEGO_HORA]) {
                        SFCriterioConfiguracionRiegoHora *criterioConfiguracion = [SFCriterioConfiguracionRiegoHora new];
                        
                        criterioConfiguracion.nombreTipoCriterioRiego = nombreTipoCriterioRiego;
                        
                        if ([datos objectForKey:@"id_criterio_riego"] != [NSNull null]) {
                            criterioConfiguracion.idCriterioRiego = [[datos objectForKey:@"id_criterio_riego"] longLongValue];
                        }
                        
                        if ([datos objectForKey:@"nombre"] != [NSNull null]) {
                            criterioConfiguracion.nombreCriterioRiego = [datos objectForKey:@"nombre"];
                        }
                        if ([datos objectForKey:@"descripcion"] != [NSNull null]) {
                            criterioConfiguracion.descripcionCriterioRiego = [datos objectForKey:@"descripcion"];
                        }
                        
                        if ([datos objectForKey:@"fechaCreacionCriterio"]!= [NSNull null]) {
                            criterioConfiguracion.fechaCreacionCriterio = [SFUtils dateFromStringYYYYMMDD:datos[@"fechaCreacionCriterio"]];
                        }
                        
                        // Valores especificos del tipo de criterio
                        
                        if ([datos objectForKey:@"numeroDia"] != [NSNull null]) {
                            criterioConfiguracion.numeroDia = [[datos objectForKey:@"numeroDia"] integerValue];
                        }
                        
                        if ([datos objectForKey:@"hora"] != [NSNull null]) {
                            criterioConfiguracion.hora = [datos objectForKey:@"hora"];
                        }
 
                        [listaCritetiosRiego addObject:criterioConfiguracion];
                    }
                    else if ([nombreTipoCriterioRiego isEqualToString:TIPO_CRITERIO_RIEGO_VOLUMEN_AGUA]){
                        SFCriterioConfiguracionRiegoVolumenAgua *criterioConfiguracion = [SFCriterioConfiguracionRiegoVolumenAgua new];
                        
                        criterioConfiguracion.nombreTipoCriterioRiego = nombreTipoCriterioRiego;
                        
                        if ([datos objectForKey:@"id_criterio_riego"] != [NSNull null]) {
                            criterioConfiguracion.idCriterioRiego = [[datos objectForKey:@"id_criterio_riego"] longLongValue];
                        }
                        
                        if ([datos objectForKey:@"nombre"] != [NSNull null]) {
                            criterioConfiguracion.nombreCriterioRiego = [datos objectForKey:@"nombre"];
                        }
                        if ([datos objectForKey:@"descripcion"] != [NSNull null]) {
                            criterioConfiguracion.descripcionCriterioRiego = [datos objectForKey:@"descripcion"];
                        }
                        
                        if ([datos objectForKey:@"fechaCreacionCriterio"]!= [NSNull null]) {
                            criterioConfiguracion.fechaCreacionCriterio = [SFUtils dateFromStringYYYYMMDD:datos[@"fechaCreacionCriterio"]];
                        }
                        
                        // Valores especificos del tipo de criterio
                        
                        if ([datos objectForKey:@"volumen"] != [NSNull null]) {
                            criterioConfiguracion.volumen = [[datos objectForKey:@"volumen"] floatValue];
                        }
                        
                        [listaCritetiosRiego addObject:criterioConfiguracion];
                    }
                }
                
                respuesta.criteriosInicialesConfiguracionRiego = listaCritetiosRiego;
                
            } @catch (NSException *exception) {
                completionBlock(respuesta);
            }
        }
        completionBlock(respuesta);
        
    } failureBlock:^(NSError *error) {
        failureBlock([BaseServicios armarErrorServicio:error]);
    }];
}

+(void) obtenerCriteriosFinalesConfiguracionRiegoMecanismoRiegoFincaSector:(SolicitudObtenerCriteriosFinalesConfiguracionRiegoMecanismoRiegoFincaSector*)solicitudObtenerCriteriosFinalesConfiguracionRiegoMecanismoRiegoFincaSector completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock{
    
    NSMutableDictionary *parametrosLlamada = [NSMutableDictionary new];
    if (solicitudObtenerCriteriosFinalesConfiguracionRiegoMecanismoRiegoFincaSector) {
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudObtenerCriteriosFinalesConfiguracionRiegoMecanismoRiegoFincaSector.idFinca] forKey:KEY_ID_FINCA];
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudObtenerCriteriosFinalesConfiguracionRiegoMecanismoRiegoFincaSector.idMecanismoRiegoFincaSector] forKey:KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR];
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudObtenerCriteriosFinalesConfiguracionRiegoMecanismoRiegoFincaSector.idConfiguracionRiego] forKey:KEY_ID_CONFIGURACION_RIEGO];
    }
    
    [[HTTPConector instance] httpOperation:OPERATION_OBTENER_CRITERIOS_FINALES_CONFIGURACION_RIEGO_MECANISMO_RIEGO_FINCA_SECTOR method:METHOD_POST withParameters:parametrosLlamada completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaObtenerCriteriosFinalesConfiguracionRiegoMecanismoRiegoFincaSector *respuesta = [RespuestaObtenerCriteriosFinalesConfiguracionRiegoMecanismoRiegoFincaSector new];
        
        NSDictionary *datosOperacion = [ServiciosModuloRiego armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        if (respuesta.resultado && datosOperacion) {
            
            @try {
                
                NSMutableArray *listaCritetiosRiego = [NSMutableArray new];
                
                for (NSDictionary *datos in datosOperacion) {
                    
                    NSString *nombreTipoCriterioRiego = @"";
                    
                    if ([datos objectForKey:@"tipo_criterio_riego"] != [NSNull null]) {
                        nombreTipoCriterioRiego = [datos objectForKey:@"tipo_criterio_riego"];
                    }
                    
                    if ([nombreTipoCriterioRiego isEqualToString:TIPO_CRITERIO_RIEGO_MEDICION]) {
                        SFCriterioConfiguracionRiegoMedicion *criterioConfiguracion = [SFCriterioConfiguracionRiegoMedicion new];
                        
                        criterioConfiguracion.nombreTipoCriterioRiego = nombreTipoCriterioRiego;
                        
                        if ([datos objectForKey:@"id_criterio_riego"] != [NSNull null]) {
                            criterioConfiguracion.idCriterioRiego = [[datos objectForKey:@"id_criterio_riego"] longLongValue];
                        }
                        
                        if ([datos objectForKey:@"nombre"] != [NSNull null]) {
                            criterioConfiguracion.nombreCriterioRiego = [datos objectForKey:@"nombre"];
                        }
                        if ([datos objectForKey:@"descripcion"] != [NSNull null]) {
                            criterioConfiguracion.descripcionCriterioRiego = [datos objectForKey:@"descripcion"];
                        }
                        
                        if ([datos objectForKey:@"fechaCreacionCriterio"]!= [NSNull null]) {
                            criterioConfiguracion.fechaCreacionCriterio = [SFUtils dateFromStringYYYYMMDD:datos[@"fechaCreacionCriterio"]];
                        }
                        
                        // Valores especificos del tipo de criterio
                        
                        if ([datos objectForKey:@"unidadMedicion"] != [NSNull null]) {
                            criterioConfiguracion.unidadMedicion = [datos objectForKey:@"unidadMedicion"];
                        }
                        if ([datos objectForKey:@"tipoMedicion"] != [NSNull null]) {
                            criterioConfiguracion.nombreTipoMedicion = [datos objectForKey:@"tipoMedicion"];
                        }
                        
                        if ([datos objectForKey:@"operador"] != [NSNull null]) {
                            criterioConfiguracion.operador = [datos objectForKey:@"operador"];
                        }
                        if ([datos objectForKey:@"valor"] != [NSNull null]) {
                            criterioConfiguracion.valor = [[datos objectForKey:@"valor"] floatValue];
                        }
                        
                        [listaCritetiosRiego addObject:criterioConfiguracion];
                    }
                    else if ([nombreTipoCriterioRiego isEqualToString:TIPO_CRITERIO_RIEGO_HORA]) {
                        SFCriterioConfiguracionRiegoHora *criterioConfiguracion = [SFCriterioConfiguracionRiegoHora new];
                        
                        criterioConfiguracion.nombreTipoCriterioRiego = nombreTipoCriterioRiego;
                        
                        if ([datos objectForKey:@"id_criterio_riego"] != [NSNull null]) {
                            criterioConfiguracion.idCriterioRiego = [[datos objectForKey:@"id_criterio_riego"] longLongValue];
                        }
                        
                        if ([datos objectForKey:@"nombre"] != [NSNull null]) {
                            criterioConfiguracion.nombreCriterioRiego = [datos objectForKey:@"nombre"];
                        }
                        if ([datos objectForKey:@"descripcion"] != [NSNull null]) {
                            criterioConfiguracion.descripcionCriterioRiego = [datos objectForKey:@"descripcion"];
                        }
                        
                        if ([datos objectForKey:@"fechaCreacionCriterio"]!= [NSNull null]) {
                            criterioConfiguracion.fechaCreacionCriterio = [SFUtils dateFromStringYYYYMMDD:datos[@"fechaCreacionCriterio"]];
                        }
                        
                        // Valores especificos del tipo de criterio
                        
                        if ([datos objectForKey:@"numeroDia"] != [NSNull null]) {
                            criterioConfiguracion.numeroDia = [[datos objectForKey:@"numeroDia"] integerValue];
                        }
                        
                        if ([datos objectForKey:@"hora"] != [NSNull null]) {
                            criterioConfiguracion.hora = [datos objectForKey:@"hora"];
                        }
                        
                        [listaCritetiosRiego addObject:criterioConfiguracion];
                    }
                    else if ([nombreTipoCriterioRiego isEqualToString:TIPO_CRITERIO_RIEGO_VOLUMEN_AGUA]){
                        SFCriterioConfiguracionRiegoVolumenAgua *criterioConfiguracion = [SFCriterioConfiguracionRiegoVolumenAgua new];
                        
                        criterioConfiguracion.nombreTipoCriterioRiego = nombreTipoCriterioRiego;
                        
                        if ([datos objectForKey:@"id_criterio_riego"] != [NSNull null]) {
                            criterioConfiguracion.idCriterioRiego = [[datos objectForKey:@"id_criterio_riego"] longLongValue];
                        }
                        
                        if ([datos objectForKey:@"nombre"] != [NSNull null]) {
                            criterioConfiguracion.nombreCriterioRiego = [datos objectForKey:@"nombre"];
                        }
                        if ([datos objectForKey:@"descripcion"] != [NSNull null]) {
                            criterioConfiguracion.descripcionCriterioRiego = [datos objectForKey:@"descripcion"];
                        }
                        
                        if ([datos objectForKey:@"fechaCreacionCriterio"]!= [NSNull null]) {
                            criterioConfiguracion.fechaCreacionCriterio = [SFUtils dateFromStringYYYYMMDD:datos[@"fechaCreacionCriterio"]];
                        }
                        
                        // Valores especificos del tipo de criterio
                        
                        if ([datos objectForKey:@"volumen"] != [NSNull null]) {
                            criterioConfiguracion.volumen = [[datos objectForKey:@"volumen"] floatValue];
                        }
                        
                        [listaCritetiosRiego addObject:criterioConfiguracion];
                    }
                }
                respuesta.criteriosFinalesConfiguracionRiego = listaCritetiosRiego;
                
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
