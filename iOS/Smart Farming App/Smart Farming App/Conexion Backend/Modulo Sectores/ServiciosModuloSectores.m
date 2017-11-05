//
//  ServiciosModuloSectores.m
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/18/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "ServiciosModuloSectores.h"

#pragma mark - operaciones

#define OPERATION_MOSTRAR_SECTORES                  @"mostrarSectores"
#define OPERATION_BUSCAR_SECTOR_ID                  @"buscarSectorId"

#define OPERATION_MOSTRAR_CULTIVO_SECTOR            @"mostrarCultivoSector"
#define OPERATION_MOSTRAR_CULTIVO_SECTOR_HISTORICO  @"mostrarCultivoSectorHistorico"

#define OPERATION_MOSTRAR_MECANISMO_RIEGO_SECTOR    @"mostrarMecanismoRiegoSector"

#define OPERATION_MOSTRAR_COMPONENTE_SENSOR_SECTOR  @"mostrarComponenteSensorSector"

@implementation ServiciosModuloSectores

+(void) mostrarSectores:(SolicitudMostrarSectores*)solicitudMostrarSectores completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock {
    
    NSMutableDictionary *parametrosLlamada = [NSMutableDictionary new];
    if (solicitudMostrarSectores.idFinca) {
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudMostrarSectores.idFinca] forKey:KEY_ID_FINCA];
    }
    
    [[HTTPConector instance] httpOperation:OPERATION_MOSTRAR_SECTORES method:METHOD_POST withParameters:parametrosLlamada completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaMostrarSectores *respuesta = [RespuestaMostrarSectores new];
        
        NSDictionary *datosOperacion = [ServiciosModuloSectores armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        if (respuesta.resultado && datosOperacion) {
            
            @try {
                NSMutableArray *sectores = [NSMutableArray new];
               
                for (NSDictionary *datos in datosOperacion) {
                    
                    SFSectorFinca *sectorFinca = [SFSectorFinca new];
                    
                    if ([datos objectForKey:KEY_ID_SECTOR] != [NSNull null]) {
                        sectorFinca.idSector = [[datos objectForKey:KEY_ID_SECTOR] longLongValue];
                    }
                    if ([datos objectForKey:KEY_NUMERO_SECTOR] != [NSNull null]) {
                        sectorFinca.numeroSector = [[datos objectForKey:KEY_NUMERO_SECTOR] integerValue];
                    }
                    
                    if ([datos objectForKey:KEY_NOMBRE_SECTOR] != [NSNull null]) {
                        sectorFinca.nombreSector = [datos objectForKey:KEY_NOMBRE_SECTOR];
                    }
                    if ([datos objectForKey:KEY_DESCRIPCION_SECTOR] != [NSNull null]) {
                        sectorFinca.descripcionSector = [datos objectForKey:KEY_DESCRIPCION_SECTOR];
                    }
                    
                    if ([datos objectForKey:KEY_SUPERFICIE_SECTOR] != [NSNull null]) {
                        sectorFinca.superficieSector = [[datos objectForKey:KEY_SUPERFICIE_SECTOR] floatValue];
                    }
                    
                    [sectores addObject:sectorFinca];
                }
                respuesta.sectores = sectores;
                
            } @catch (NSException *exception) {
                completionBlock(respuesta);
            }
        }
        completionBlock(respuesta);

    } failureBlock:^(NSError *error) {
        failureBlock([BaseServicios armarErrorServicio:error]);
    }];
}

+(void) buscarSectorId:(SolicitudBuscarSectorId*)solicitudBuscarSectorId completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock {
    
    NSMutableDictionary *parametrosLlamada = [NSMutableDictionary new];
    if (solicitudBuscarSectorId.idSector) {
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudBuscarSectorId.idSector] forKey:KEY_ID_SECTOR];
    }
    
    [[HTTPConector instance] httpOperation:OPERATION_BUSCAR_SECTOR_ID method:METHOD_POST withParameters:parametrosLlamada completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaBuscarSectorId *respuesta = [RespuestaBuscarSectorId new];
        
        NSDictionary *datosOperacion = [ServiciosModuloSectores armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        if (respuesta.resultado && datosOperacion) {
            
            @try {
                SFSectorFinca *sectorFinca = [SFSectorFinca new];
                
                if ([datosOperacion objectForKey:KEY_ID_SECTOR] != [NSNull null]) {
                    sectorFinca.idSector = [[datosOperacion objectForKey:KEY_ID_SECTOR] longLongValue];
                }
                if ([datosOperacion objectForKey:KEY_NUMERO_SECTOR] != [NSNull null]) {
                    sectorFinca.numeroSector = [[datosOperacion objectForKey:KEY_NUMERO_SECTOR] integerValue];
                }
                
                if ([datosOperacion objectForKey:KEY_NOMBRE_SECTOR] != [NSNull null]) {
                    sectorFinca.nombreSector = [datosOperacion objectForKey:KEY_NOMBRE_SECTOR];
                }
                if ([datosOperacion objectForKey:KEY_DESCRIPCION_SECTOR] != [NSNull null]) {
                    sectorFinca.descripcionSector = [datosOperacion objectForKey:KEY_DESCRIPCION_SECTOR];
                }
                
                if ([datosOperacion objectForKey:KEY_SUPERFICIE_SECTOR] != [NSNull null]) {
                    sectorFinca.superficieSector = [[datosOperacion objectForKey:KEY_SUPERFICIE_SECTOR] floatValue];
                }
                
                respuesta.sector = sectorFinca;
                
            } @catch (NSException *exception) {
                completionBlock(respuesta);
            }
        }
        completionBlock(respuesta);
    } failureBlock:^(NSError *error) {
        failureBlock([BaseServicios armarErrorServicio:error]);
    }];
}

+(void) mostrarCultivoSector:(SolicitudMostrarCultivoSector*)solicitudMostrarCultivoSector
             completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock {
    
    NSMutableDictionary *parametrosLlamada = [NSMutableDictionary new];
    if (solicitudMostrarCultivoSector.idSector) {
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudMostrarCultivoSector.idSector] forKey:KEY_ID_SECTOR];
    }
    
    [[HTTPConector instance] httpOperation:OPERATION_MOSTRAR_CULTIVO_SECTOR method:METHOD_POST withParameters:parametrosLlamada completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaMostrarCultivoSector *respuesta = [RespuestaMostrarCultivoSector new];
        
        NSDictionary *datosOperacion = [ServiciosModuloSectores armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        if (respuesta.resultado && datosOperacion) {
            
            @try {
                SFCultivoSector *cultivoSector = [SFCultivoSector new];
                
                if ([datosOperacion objectForKey:KEY_ID_CULTIVO] != [NSNull null]) {
                    cultivoSector.idCultivoSector = [[datosOperacion objectForKey:KEY_ID_CULTIVO] longLongValue];
                }
                
                if ([datosOperacion objectForKey:KEY_NOMBRE_CULTIVO_SECTOR] != [NSNull null]) {
                    cultivoSector.nombreCultivoSector = [datosOperacion objectForKey:KEY_NOMBRE_CULTIVO_SECTOR];
                }
                if ([datosOperacion objectForKey:KEY_DESCRIPCION_CULTIVO_SECTOR] != [NSNull null]) {
                    cultivoSector.descripcionCultivoSector = [datosOperacion objectForKey:KEY_DESCRIPCION_CULTIVO_SECTOR];
                }
                
                if ([datosOperacion objectForKey:KEY_SUBTIPO_CULTIVO_SECTOR] != [NSNull null]) {
                    cultivoSector.subTipoCultivo = [datosOperacion objectForKey:KEY_SUBTIPO_CULTIVO_SECTOR];
                }
                if ([datosOperacion objectForKey:KEY_TIPO_CULTIVO_SECTOR] != [NSNull null]) {
                    cultivoSector.tipoCultivo = [datosOperacion objectForKey:KEY_TIPO_CULTIVO_SECTOR];
                }
                
                if ([datosOperacion objectForKey:KEY_FECHA_PLANTACION_CULTIVO_SECTOR] != [NSNull null]) {
                    cultivoSector.fechaPlantacionCultivoSector = [SFUtils dateFromStringYYYYMMDDWithTime:datosOperacion[KEY_FECHA_PLANTACION_CULTIVO_SECTOR]];
                }
                if ([datosOperacion objectForKey:KEY_FECHA_ELIMINACION_CULTIVO_SECTOR] != [NSNull null]) {
                    cultivoSector.fechaEliminacionCultivoSector = [SFUtils dateFromStringYYYYMMDD:datosOperacion[KEY_FECHA_ELIMINACION_CULTIVO_SECTOR]];
                }
                
                if ([datosOperacion objectForKey:KEY_HABILITADO_CULTIVO_SECTOR] != [NSNull null]) {
                    NSString *habilitado = [datosOperacion objectForKey:KEY_HABILITADO_CULTIVO_SECTOR];
                    if (habilitado) {
                        cultivoSector.habilitado = [habilitado boolValue];
                    }
                }
                respuesta.cultivoSector = cultivoSector;
                
            } @catch (NSException *exception) {
                completionBlock(respuesta);
            }
        }
        completionBlock(respuesta);
    } failureBlock:^(NSError *error) {
        failureBlock([BaseServicios armarErrorServicio:error]);
    }];
}

+(void) mostrarCultivoSectorHistorico:(SolicitudMostrarCultivoSectorHistorico*)solicitudMostrarCultivoSectorHistorico completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock {
    
    NSMutableDictionary *parametrosLlamada = [NSMutableDictionary new];
    if (solicitudMostrarCultivoSectorHistorico.idSector) {
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudMostrarCultivoSectorHistorico.idSector] forKey:KEY_ID_SECTOR];
    }
    
    [[HTTPConector instance] httpOperation:OPERATION_MOSTRAR_CULTIVO_SECTOR_HISTORICO method:METHOD_POST withParameters:parametrosLlamada completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaMostrarCultivoSectorHistorico *respuesta = [RespuestaMostrarCultivoSectorHistorico new];
        
        NSDictionary *datosOperacion = [ServiciosModuloSectores armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        if (respuesta.resultado && datosOperacion) {
            
            @try {
                NSMutableArray *cultivosSector = [NSMutableArray new];
                
                for (NSDictionary *datos in datosOperacion) {
                    
                    SFCultivoSector *cultivoSector = [SFCultivoSector new];
                    
                    if ([datos objectForKey:KEY_ID_CULTIVO] != [NSNull null]) {
                        cultivoSector.idCultivoSector = [[datos objectForKey:KEY_ID_CULTIVO] longLongValue];
                    }
                    
                    if ([datos objectForKey:KEY_NOMBRE_CULTIVO_SECTOR] != [NSNull null]) {
                        cultivoSector.nombreCultivoSector = [datos objectForKey:KEY_NOMBRE_CULTIVO_SECTOR];
                    }
                    if ([datos objectForKey:KEY_DESCRIPCION_CULTIVO_SECTOR] != [NSNull null]) {
                        cultivoSector.descripcionCultivoSector = [datos objectForKey:KEY_DESCRIPCION_CULTIVO_SECTOR];
                    }
                    
                    if ([datos objectForKey:KEY_SUBTIPO_CULTIVO_SECTOR] != [NSNull null]) {
                        cultivoSector.subTipoCultivo = [datos objectForKey:KEY_SUBTIPO_CULTIVO_SECTOR];
                    }
                    if ([datos objectForKey:KEY_TIPO_CULTIVO_SECTOR] != [NSNull null]) {
                        cultivoSector.subTipoCultivo = [datos objectForKey:KEY_TIPO_CULTIVO_SECTOR];
                    }
                    
                    if ([datos objectForKey:KEY_FECHA_PLANTACION_CULTIVO_SECTOR] != [NSNull null]) {
                        cultivoSector.fechaPlantacionCultivoSector = [SFUtils dateFromStringYYYYMMDD:datos[KEY_FECHA_PLANTACION_CULTIVO_SECTOR]];
                    }
                    if ([datos objectForKey:KEY_FECHA_ELIMINACION_CULTIVO_SECTOR] != [NSNull null]) {
                        cultivoSector.fechaEliminacionCultivoSector = [SFUtils dateFromStringYYYYMMDD:datos[KEY_FECHA_ELIMINACION_CULTIVO_SECTOR]];
                    }
                    
                    if ([datos objectForKey:KEY_HABILITADO_CULTIVO_SECTOR] != [NSNull null]) {
                        NSString *habilitado = [datos objectForKey:KEY_HABILITADO_CULTIVO_SECTOR];
                        if (habilitado) {
                            cultivoSector.habilitado = [habilitado boolValue];
                        }
                    }
                    
                    [cultivosSector addObject:cultivoSector];
                }
                respuesta.cultivosSector = cultivosSector;
                
            } @catch (NSException *exception) {
                completionBlock(respuesta);
            }
        }
        completionBlock(respuesta);
    } failureBlock:^(NSError *error) {
        failureBlock([BaseServicios armarErrorServicio:error]);
    }];
}

+(void) mostrarMecanismoRiegoSector:(SolicitudMostrarMecanismoRiegoSector*)solicitudMostrarMecanismoRiegoSector completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock {
    
    NSMutableDictionary *parametrosLlamada = [NSMutableDictionary new];
    if (solicitudMostrarMecanismoRiegoSector.idSector) {
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudMostrarMecanismoRiegoSector.idSector] forKey:KEY_ID_SECTOR];
    }
    
    [[HTTPConector instance] httpOperation:OPERATION_MOSTRAR_MECANISMO_RIEGO_SECTOR method:METHOD_POST withParameters:parametrosLlamada completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaMostrarMecanismoRiegoSector *respuesta = [RespuestaMostrarMecanismoRiegoSector new];
        
        NSDictionary *datosOperacion = [ServiciosModuloSectores armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        if (respuesta.resultado && datosOperacion) {
            
            @try {
                SFMecanismoRiegoFincaSector *mecanismoRiegoFincaSector = [SFMecanismoRiegoFincaSector new];
                
                if ([datosOperacion objectForKey:KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR] != [NSNull null]) {
                    mecanismoRiegoFincaSector.idMecanismoRiegoFincaSector = [[datosOperacion objectForKey:KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR] longLongValue];
                }
                
                if ([datosOperacion objectForKey:KEY_ID_FINCA] != [NSNull null]) {
                    mecanismoRiegoFincaSector.idFinca = [[datosOperacion objectForKey:KEY_ID_FINCA] longLongValue];
                }
                if ([datosOperacion objectForKey:KEY_ID_MECANISMO_RIEGO_FINCA] != [NSNull null]) {
                    mecanismoRiegoFincaSector.idMecanismoRiegoFinca = [[datosOperacion objectForKey:KEY_ID_MECANISMO_RIEGO_FINCA] longLongValue];
                }
                if ([datosOperacion objectForKey:KEY_ID_SECTOR] != [NSNull null]) {
                    mecanismoRiegoFincaSector.idSector = [[datosOperacion objectForKey:KEY_ID_SECTOR] longLongValue];
                }
                
                if ([datosOperacion objectForKey:KEY_NOMBRE_TIPO_MECANISMO] != [NSNull null]) {
                    mecanismoRiegoFincaSector.nombreTipoMecanismo = [datosOperacion objectForKey:KEY_NOMBRE_TIPO_MECANISMO];
                }
                
                if ([datosOperacion objectForKey:KEY_MECANISMO_RIEGO_CAUDAL_RESPUESTA] != [NSNull null]) {
                    mecanismoRiegoFincaSector.caudal = [[datosOperacion objectForKey:KEY_MECANISMO_RIEGO_CAUDAL_RESPUESTA] floatValue];
                }
                if ([datosOperacion objectForKey:KEY_MECANISMO_RIEGO_PRESION_RESPUESTA] != [NSNull null]) {
                    mecanismoRiegoFincaSector.presion = [[datosOperacion objectForKey:KEY_MECANISMO_RIEGO_PRESION_RESPUESTA] floatValue];
                }
                
                respuesta.mecanismoRiegoFincaSector = mecanismoRiegoFincaSector;
                
            } @catch (NSException *exception) {
                completionBlock(respuesta);
            }
        }
        completionBlock(respuesta);
    } failureBlock:^(NSError *error) {
        failureBlock([BaseServicios armarErrorServicio:error]);
    }];
}

+(void) mostrarComponenteSensorSector:(SolcitudMostrarComponenteSensorSector*)solcitudMostrarComponenteSensorSector completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock {
    
    NSMutableDictionary *parametrosLlamada = [NSMutableDictionary new];
    if (solcitudMostrarComponenteSensorSector.idSector) {
        [parametrosLlamada setObject:[NSNumber numberWithLong:solcitudMostrarComponenteSensorSector.idSector] forKey:KEY_ID_SECTOR];
    }
    
    [[HTTPConector instance] httpOperation:OPERATION_MOSTRAR_COMPONENTE_SENSOR_SECTOR method:METHOD_POST withParameters:parametrosLlamada completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaMostrarComponenteSensorSector *respuesta = [RespuestaMostrarComponenteSensorSector new];
        
        NSDictionary *datosOperacion = [ServiciosModuloSectores armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        if (respuesta.resultado && datosOperacion) {
            
            @try {
                SFComponenteSensor *componenteSensor = [SFComponenteSensor new];
                
                if ([datosOperacion objectForKey:KEY_ID_COMPONENTE_SENSOR] != [NSNull null]) {
                    componenteSensor.idComponenteSensor = [[datosOperacion objectForKey:KEY_ID_COMPONENTE_SENSOR] longLongValue];
                }
                if ([datosOperacion objectForKey:KEY_FINCA_COMPONENTE_SENSOR_RESPUESTA] != [NSNull null]) {
                    componenteSensor.idFinca = [[datosOperacion objectForKey:KEY_FINCA_COMPONENTE_SENSOR_RESPUESTA] longLongValue];
                }
                
                if ([datosOperacion objectForKey:KEY_MODELO_COMPONENTE_SENSOR_RESPUESTA] != [NSNull null]) {
                    componenteSensor.modelo = [datosOperacion objectForKey:KEY_MODELO_COMPONENTE_SENSOR_RESPUESTA];
                }
                if ([datosOperacion objectForKey:KEY_DESCRIPCION_COMPONENTE_SENSOR_RESPUESTA] != [NSNull null]) {
                    componenteSensor.descripcion = [datosOperacion objectForKey:KEY_DESCRIPCION_COMPONENTE_SENSOR_RESPUESTA];
                }
                
                if ([datosOperacion objectForKey:KEY_ESTADO_COMPONENTE_SENSOR_RESPUESTA] != [NSNull null]) {
                    componenteSensor.estadoComponenteSensor = [datosOperacion objectForKey:KEY_ESTADO_COMPONENTE_SENSOR_RESPUESTA];
                }
                
                if ([datosOperacion objectForKey:KEY_CANTIDAD_MAXIMA_SENSORES] != [NSNull null]) {
                    componenteSensor.cantidadMaximaSensores = [[datosOperacion objectForKey:KEY_CANTIDAD_MAXIMA_SENSORES] integerValue];
                }
                if ([datosOperacion objectForKey:KEY_CANTIDAD_SENSORES_ASIGNADOS] != [NSNull null]) {
                    componenteSensor.cantidadSensoresAsignados = [[datosOperacion objectForKey:KEY_CANTIDAD_SENSORES_ASIGNADOS] integerValue];
                }
                
                respuesta.componenteSensor = componenteSensor;
                
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
