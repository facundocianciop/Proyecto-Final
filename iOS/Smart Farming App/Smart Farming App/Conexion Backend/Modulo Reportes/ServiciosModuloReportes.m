//
//  ServiciosModuloReportes.m
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/24/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "ServiciosModuloReportes.h"

#pragma mark - operaciones

#define OPERATION_BUSCAR_CONFIGURACIONES_EVENTOS_PERSONALIZADOS @"buscarConfiguracionesEventosPersonalizadosSector"
#define OPERATION_MOSTRAR_CONFIGURACION_EVENTO_PERSONALIZADO    @"mostrarConfiguracionEventoPersonalizado"

#define OPERATION_OBTENER_ESTADO_ACTUAL_SECTOR                  @"obtenerEstadoActualSector"
#define OPERATION_OBTENER_INFORME_HISTORICO_SECTOR              @"obtenerInformeHistoricoSector"
#define OPERATION_OBTENER_INFORME_RIEGO_EJECUCION_SECTOR        @"obtenerInformeRiegoEjecucionSector"
#define OPERATION_OBTENER_INFORME_RIEGO_HISTORICO_SECTOR        @"obtenerInformeRiegoHistoricoSector"
#define OPERATION_OBTENER_INFORME_EVENTOS_PERSONALIZADOS        @"obtenerInformeEventosPersonalizados"
#define OPERATION_OBTENER_INFORME_HISTORICO_HELADAS             @"obtenerInformeHistoricoHeladas"
#define OPERATION_OBTENER_INFORME_CRUZADO_RIEGO_MEDICIONES      @"obtenerInformeCruzadoRiegoMediciones"
    
@implementation ServiciosModuloReportes

+(void) buscarConfiguracionesEventosPersonalizados:(SolicitudBuscarConfiguracionesEventosPersonalizados*)solicitudBuscarConfiguracionesEventosPersonalizados completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock {
    
    NSMutableDictionary *parametrosLlamada = [NSMutableDictionary new];
    if (solicitudBuscarConfiguracionesEventosPersonalizados) {
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudBuscarConfiguracionesEventosPersonalizados.idFinca] forKey:KEY_ID_FINCA];
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudBuscarConfiguracionesEventosPersonalizados.idUsuarioFinca] forKey:KEY_ID_USUARIO_FINCA];
         [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudBuscarConfiguracionesEventosPersonalizados.idSector] forKey:KEY_ID_SECTOR];
    }
    
    [[HTTPConector instance] httpOperation:OPERATION_BUSCAR_CONFIGURACIONES_EVENTOS_PERSONALIZADOS method:METHOD_POST withParameters:parametrosLlamada completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaBuscarConfiguracionesEventosPersonalizados *respuesta = [RespuestaBuscarConfiguracionesEventosPersonalizados new];
        
        NSDictionary *datosOperacion = [ServiciosModuloReportes armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        if (respuesta.resultado && datosOperacion) {
            
            @try {
                
                NSMutableArray *listaInstancias = [NSMutableArray new];
                
                for (NSDictionary *datos in datosOperacion[@"dto_evento_lista"]) {
                    
                    SFConfiguracionEvento *nuevaInstancia = [SFConfiguracionEvento new];
                    
                    if ([datos objectForKey:@"id_usuario_finca"] != [NSNull null]) {
                        nuevaInstancia.idUsuarioFinca = [[datos objectForKey:@"id_usuario_finca"] longLongValue];
                    }
                    if ([datos objectForKey:@"id_configuracion_evento"] != [NSNull null]) {
                        nuevaInstancia.idConfiguracionEvento = [[datos objectForKey:@"id_configuracion_evento"] longLongValue];
                    }
                    if ([datos objectForKey:@"id_sector"] != [NSNull null]) {
                        nuevaInstancia.idSector = (long)[datos objectForKey:@"id_sector"];
                    }
                    
                    if ([datos objectForKey:@"nombre"] != [NSNull null]) {
                        nuevaInstancia.nombreConfiguracioEvento = [datos objectForKey:@"nombre"];
                    }
                    if ([datos objectForKey:@"descripcion"] != [NSNull null]) {
                        nuevaInstancia.descripcionConfiguracioEvento = [datos objectForKey:@"descripcion"];
                    }
      
                    if ([datos objectForKey:@"fecha_hora_creacion"]!= [NSNull null]) {
                        nuevaInstancia.fechaHoraCreacion = [SFUtils dateFromStringYYYYMMDDWithTime:datos[@"fecha_hora_creacion"]];
                    }
                    
                    if ([datos objectForKey:@"activado"] != [NSNull null]) {
                        nuevaInstancia.activado = [[datos objectForKey:@"activado"] boolValue];
                    }
                    if ([datos objectForKey:@"notificacion_activada"] != [NSNull null]) {
                        nuevaInstancia.notificacionActivada = [[datos objectForKey:@"notificacion_activada"] boolValue];
                    }
                    
                    if ([datos objectForKey:@"lista_mediciones_internas"] != [NSNull null]) {
                        NSDictionary *datosMedicionesInternas = [datos objectForKey:@"lista_mediciones_internas"];
                        
                        NSMutableArray<SFMedicionFuenteInterna*> *listaNuevasMedicionesInternas = [NSMutableArray new];
                        for (NSDictionary *datoMedicionInterna in datosMedicionesInternas) {
                            
                            SFMedicionFuenteInterna *medicionInterna = [SFMedicionFuenteInterna new];
                            
                            if ([datoMedicionInterna objectForKey:@"tipo_medicion"] != [NSNull null]) {
                                medicionInterna.nombreTipoMedicion = [datoMedicionInterna objectForKey:@"tipo_medicion"];
                            }
                            if ([datoMedicionInterna objectForKey:@"unidad_medicion"] != [NSNull null]) {
                                medicionInterna.unidadMedicion = [datoMedicionInterna objectForKey:@"unidad_medicion"];
                            }
                            
                            if ([datoMedicionInterna objectForKey:@"valor_maximo"] != [NSNull null]) {
                                medicionInterna.valorMaximo = [[datoMedicionInterna objectForKey:@"valor_maximo"] floatValue];
                            }
                            if ([datoMedicionInterna objectForKey:@"valor_minimo"] != [NSNull null]) {
                                medicionInterna.valorMinimo = [[datoMedicionInterna objectForKey:@"valor_minimo"] floatValue];
                            }
                                                        
                            [listaNuevasMedicionesInternas addObject:medicionInterna];
                        }
                        nuevaInstancia.listaMedicionesInternas = [NSArray arrayWithArray:listaNuevasMedicionesInternas];
                    }
                    
                    if ([datos objectForKey:@"lista_mediciones_externas"] != [NSNull null]) {
                        NSDictionary *datosMedicionesExternas = [datos objectForKey:@"lista_mediciones_externas"];
                        
                        NSMutableArray<SFMedicionFuenteExterna*> *listaNuevasMedicionesExternas = [NSMutableArray new];
                        for (NSDictionary *datoMedicionExterna in datosMedicionesExternas) {
                            
                            SFMedicionFuenteExterna *medicionExterna = [SFMedicionFuenteExterna new];
                            
                            if ([datoMedicionExterna objectForKey:@"tipo_medicion"] != [NSNull null]) {
                                medicionExterna.nombreTipoMedicion = [datoMedicionExterna objectForKey:@"tipo_medicion"];
                            }
                            if ([datoMedicionExterna objectForKey:@"unidad_medicion"] != [NSNull null]) {
                                medicionExterna.unidadMedicion = [datoMedicionExterna objectForKey:@"unidad_medicion"];
                            }
                            
                            if ([datoMedicionExterna objectForKey:@"valor_maximo"] != [NSNull null]) {
                                medicionExterna.valorMaximo = [[datoMedicionExterna objectForKey:@"valor_maximo"] floatValue];
                            }
                            if ([datoMedicionExterna objectForKey:@"valor_minimo"] != [NSNull null]) {
                                medicionExterna.valorMinimo = [[datoMedicionExterna objectForKey:@"valor_minimo"] floatValue];
                            }
                            
                            [listaNuevasMedicionesExternas addObject:medicionExterna];
                        }
                        nuevaInstancia.listaMedicionesExternas = [NSArray arrayWithArray:listaNuevasMedicionesExternas];
                    }
            
                    [listaInstancias addObject:nuevaInstancia];
                }
                
                respuesta.configuracionesEvento = listaInstancias;
                
            } @catch (NSException *exception) {
                completionBlock(respuesta);
            }
        }
        completionBlock(respuesta);
     
    } failureBlock:^(NSError *error) {
        failureBlock([BaseServicios armarErrorServicio:error]);
    }];
}

+(void) mostrarConfiguracionEventoPersonalizado:(SolicitudMostrarConfiguracionEventoPersonalizado*)solicitudMostrarConfiguracionEventoPersonalizado completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock{
    
    NSMutableDictionary *parametrosLlamada = [NSMutableDictionary new];
    if (solicitudMostrarConfiguracionEventoPersonalizado) {
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudMostrarConfiguracionEventoPersonalizado.idFinca] forKey:KEY_ID_FINCA];
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudMostrarConfiguracionEventoPersonalizado.idConfiguracionEvento] forKey:KEY_ID_CONFIGURACION_EVENTO_PERSONALIZADO];
    }
    
    [[HTTPConector instance] httpOperation:OPERATION_MOSTRAR_CONFIGURACION_EVENTO_PERSONALIZADO method:METHOD_POST withParameters:parametrosLlamada completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaMostrarConfiguracionEventoPersonalizado *respuesta = [RespuestaMostrarConfiguracionEventoPersonalizado new];
        
        NSDictionary *datosOperacion = [ServiciosModuloReportes armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        if (respuesta.resultado && datosOperacion) {
            
            @try {
                
                SFConfiguracionEvento *nuevaInstancia = [SFConfiguracionEvento new];
                
                if ([datosOperacion objectForKey:@"id_usuario_finca"] != [NSNull null]) {
                    nuevaInstancia.idUsuarioFinca = [[datosOperacion objectForKey:@"id_usuario_finca"] longLongValue];
                }
                if ([datosOperacion objectForKey:@"id_configuracion_evento"] != [NSNull null]) {
                    nuevaInstancia.idConfiguracionEvento = [[datosOperacion objectForKey:@"id_configuracion_evento"] longLongValue];
                }
                if ([datosOperacion objectForKey:@"id_sector"] != [NSNull null]) {
                    nuevaInstancia.idSector = [[datosOperacion objectForKey:@"id_sector"] longLongValue];
                }
                
                if ([datosOperacion objectForKey:@"nombre"] != [NSNull null]) {
                    nuevaInstancia.nombreConfiguracioEvento = [datosOperacion objectForKey:@"nombre"];
                }
                if ([datosOperacion objectForKey:@"descripcion"] != [NSNull null]) {
                    nuevaInstancia.descripcionConfiguracioEvento = [datosOperacion objectForKey:@"descripcion"];
                }
                
                if ([datosOperacion objectForKey:@"fecha_hora_creacion"]!= [NSNull null]) {
                    nuevaInstancia.fechaHoraCreacion = [SFUtils dateFromStringYYYYMMDDWithTime:datosOperacion[@"fecha_hora_creacion"]];
                }
                
                if ([datosOperacion objectForKey:@"activado"] != [NSNull null]) {
                    nuevaInstancia.activado = [[datosOperacion objectForKey:@"activado"] boolValue];
                }
                if ([datosOperacion objectForKey:@"notificacion_activada"] != [NSNull null]) {
                    nuevaInstancia.notificacionActivada = [[datosOperacion objectForKey:@"notificacion_activada"] boolValue];
                }
                
                if ([datosOperacion objectForKey:@"lista_mediciones_internas"] != [NSNull null]) {
                    NSDictionary *datosMedicionesInternas = [datosOperacion objectForKey:@"lista_mediciones_internas"];
                    
                    NSMutableArray<SFMedicionFuenteInterna*> *listaNuevasMedicionesInternas = [NSMutableArray new];
                    for (NSDictionary *datoMedicionInterna in datosMedicionesInternas) {
                        
                        SFMedicionFuenteInterna *medicionInterna = [SFMedicionFuenteInterna new];
                        
                        if ([datoMedicionInterna objectForKey:@"tipo_medicion"] != [NSNull null]) {
                            medicionInterna.nombreTipoMedicion = [datoMedicionInterna objectForKey:@"tipo_medicion"];
                        }
                        if ([datoMedicionInterna objectForKey:@"unidad_medicion"] != [NSNull null]) {
                            medicionInterna.unidadMedicion = [datoMedicionInterna objectForKey:@"unidad_medicion"];
                        }
                        
                        if ([datoMedicionInterna objectForKey:@"valor_maximo"] != [NSNull null]) {
                            medicionInterna.valorMaximo = [[datoMedicionInterna objectForKey:@"valor_maximo"] floatValue];
                        }
                        if ([datoMedicionInterna objectForKey:@"valor_minimo"] != [NSNull null]) {
                            medicionInterna.valorMinimo = [[datoMedicionInterna objectForKey:@"valor_minimo"] floatValue];
                        }
                        
                        [listaNuevasMedicionesInternas addObject:medicionInterna];
                    }
                    nuevaInstancia.listaMedicionesInternas = [NSArray arrayWithArray:listaNuevasMedicionesInternas];
                }
                
                if ([datosOperacion objectForKey:@"lista_mediciones_externas"] != [NSNull null]) {
                    NSDictionary *datosMedicionesExternas = [datosOperacion objectForKey:@"lista_mediciones_externas"];
                    
                    NSMutableArray<SFMedicionFuenteExterna*> *listaNuevasMedicionesExternas = [NSMutableArray new];
                    for (NSDictionary *datoMedicionExterna in datosMedicionesExternas) {
                        
                        SFMedicionFuenteExterna *medicionExterna = [SFMedicionFuenteExterna new];
                        
                        if ([datoMedicionExterna objectForKey:@"tipo_medicion"] != [NSNull null]) {
                            medicionExterna.nombreTipoMedicion = [datoMedicionExterna objectForKey:@"tipo_medicion"];
                        }
                        if ([datoMedicionExterna objectForKey:@"unidad_medicion"] != [NSNull null]) {
                            medicionExterna.unidadMedicion = [datoMedicionExterna objectForKey:@"unidad_medicion"];
                        }
                        
                        if ([datoMedicionExterna objectForKey:@"valor_maximo"] != [NSNull null]) {
                            medicionExterna.valorMaximo = [[datoMedicionExterna objectForKey:@"valor_maximo"] floatValue];
                        }
                        if ([datoMedicionExterna objectForKey:@"valor_minimo"] != [NSNull null]) {
                            medicionExterna.valorMinimo = [[datoMedicionExterna objectForKey:@"valor_minimo"] floatValue];
                        }
                        
                        [listaNuevasMedicionesExternas addObject:medicionExterna];
                    }
                    nuevaInstancia.listaMedicionesExternas = [NSArray arrayWithArray: listaNuevasMedicionesExternas];
                }
                
                respuesta.configuracionEvento = nuevaInstancia;
                
            } @catch (NSException *exception) {
                completionBlock(respuesta);
            }
        }
        completionBlock(respuesta);
        
    } failureBlock:^(NSError *error) {
        failureBlock([BaseServicios armarErrorServicio:error]);
    }];
    
}

+(void) obtenerEstadoActualSector:(SolicitudObtenerEstadoActualSector*)solicitudObtenerEstadoActualSector completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock {
    
    NSMutableDictionary *parametrosLlamada = [NSMutableDictionary new];
    if (solicitudObtenerEstadoActualSector) {
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudObtenerEstadoActualSector.idFinca] forKey:KEY_ID_FINCA];
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudObtenerEstadoActualSector.idSector] forKey:KEY_ID_SECTOR];
    }
    
    [[HTTPConector instance] httpOperation:OPERATION_OBTENER_ESTADO_ACTUAL_SECTOR method:METHOD_POST withParameters:parametrosLlamada completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaObtenerEstadoActualSector *respuesta = [RespuestaObtenerEstadoActualSector new];
        
        NSDictionary *datosOperacion = [ServiciosModuloReportes armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        if (respuesta.resultado && datosOperacion) {
            
            @try {
                
                if ([datosOperacion objectForKey:@"id_sector"] != [NSNull null]) {
                    respuesta.idSector = [[datosOperacion objectForKey:@"id_sector"] longLongValue];
                }
                
                if ([datosOperacion objectForKey:@"numero_sector"] != [NSNull null]) {
                    respuesta.nroSector = [[datosOperacion objectForKey:@"numero_sector"] integerValue];
                }
                
                if ([datosOperacion objectForKey:@"descripcion_sector"] != [NSNull null]) {
                    respuesta.descripcionSector = [datosOperacion objectForKey:@"descripcion_sector"];
                }
                if ([datosOperacion objectForKey:@"superficie_sector"] != [NSNull null]) {
                    respuesta.superficieSector = [[datosOperacion objectForKey:@"superficie_sector"] floatValue];
                }
                
                if ([datosOperacion objectForKey:@"componente_sector"] != [NSNull null]) {
                    NSDictionary *datos = [datosOperacion objectForKey:@"componente_sector"];
                    
                    SFComponenteSensor *componenteSensorSector = [SFComponenteSensor new];
                    
                    if ([datos objectForKey:@"idComponenteSensor"] != [NSNull null]) {
                        componenteSensorSector.idComponenteSensor = [[datos objectForKey:@"idComponenteSensor"] longLongValue];
                    }
                    
                    if ([datos objectForKey:@"finca"] != [NSNull null]) {
                        componenteSensorSector.idFinca = [[datos objectForKey:@"finca"] longLongValue];
                    }
                    
                    if ([datos objectForKey:@"modelo"] != [NSNull null]) {
                        componenteSensorSector.modelo = [datos objectForKey:@"modelo"];
                    }
                    if ([datos objectForKey:@"descripcion"] != [NSNull null]) {
                        componenteSensorSector.descripcion = [datos objectForKey:@"descripcion"];
                    }
                    
                    if ([datos objectForKey:@"estado"] != [NSNull null]) {
                        componenteSensorSector.estadoComponenteSensor = [datos objectForKey:@"estado"];
                    }
                    
                    if ([datos objectForKey:@"cantidadMaximaSensores"] != [NSNull null]) {
                        componenteSensorSector.cantidadMaximaSensores = [[datos objectForKey:@"cantidadMaximaSensores"] integerValue];
                    }
                    if ([datos objectForKey:@"cantidadSensoresAsignados"] != [NSNull null]) {
                        componenteSensorSector.cantidadSensoresAsignados = [[datos objectForKey:@"cantidadSensoresAsignados"] integerValue];
                    }
                    
                    respuesta.componenteSensorSector = componenteSensorSector;
                }

                if ([datosOperacion objectForKey:@"mecanismo_sector"] != [NSNull null]) {
                    NSDictionary *datos = [datosOperacion objectForKey:@"mecanismo_sector"];
                    
                    SFMecanismoRiegoFincaSector *mecanismoRiegoFincaSector = [SFMecanismoRiegoFincaSector new];
                    
                    if ([datos objectForKey:KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR] != [NSNull null]) {
                        mecanismoRiegoFincaSector.idMecanismoRiegoFincaSector = [[datos objectForKey:KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR] longLongValue];
                    }
                    
                    if ([datos objectForKey:KEY_ID_FINCA] != [NSNull null]) {
                        mecanismoRiegoFincaSector.idFinca = [[datos objectForKey:KEY_ID_FINCA] longLongValue];
                    }
                    if ([datos objectForKey:KEY_ID_MECANISMO_RIEGO_FINCA] != [NSNull null]) {
                        mecanismoRiegoFincaSector.idMecanismoRiegoFinca = [[datos objectForKey:KEY_ID_MECANISMO_RIEGO_FINCA] longLongValue];
                    }
                    if ([datos objectForKey:KEY_ID_SECTOR] != [NSNull null]) {
                        mecanismoRiegoFincaSector.idSector = [[datos objectForKey:KEY_ID_SECTOR] longLongValue];
                    }
                    
                    if ([datos objectForKey:KEY_NOMBRE_TIPO_MECANISMO] != [NSNull null]) {
                        mecanismoRiegoFincaSector.nombreTipoMecanismo = [datos objectForKey:KEY_NOMBRE_TIPO_MECANISMO];
                    }
                    
                    if ([datos objectForKey:KEY_MECANISMO_RIEGO_CAUDAL_RESPUESTA] != [NSNull null]) {
                        mecanismoRiegoFincaSector.caudal = [[datos objectForKey:KEY_MECANISMO_RIEGO_CAUDAL_RESPUESTA] floatValue];
                    }
                    if ([datos objectForKey:KEY_MECANISMO_RIEGO_PRESION_RESPUESTA] != [NSNull null]) {
                        mecanismoRiegoFincaSector.presion = [[datos objectForKey:KEY_MECANISMO_RIEGO_PRESION_RESPUESTA] floatValue];
                    }

                    respuesta.mecanismoRiegoFincaSector = mecanismoRiegoFincaSector;
                }
                
                if ([datosOperacion objectForKey:@"ultima_medicion"] != [NSNull null]) {
                    NSDictionary *datos = [datosOperacion objectForKey:@"ultima_medicion"];
                    
                    SFMedicionSensorCabecera *ultimaMedicion = [SFMedicionSensorCabecera new];
                    
                    if ([datos objectForKey:@"nro_medicion"] != [NSNull null]) {
                        ultimaMedicion.nroMedicion = [[datos objectForKey:@"nro_medicion"] integerValue];
                    }
                    
                    if ([datos objectForKey:@"fecha_y_hora"]!= [NSNull null]) {
                        ultimaMedicion.fechaYHora = [SFUtils dateFromStringYYYYMMDDWithTime: datos[@"fecha_y_hora"]];
                    }
                    
                    if ([datos objectForKey:@"lista_mediciones_detalle"]!= [NSNull null]) {
                        NSDictionary *listaInfoDetallesMediones = [datos objectForKey:@"lista_mediciones_detalle"];
                        
                        NSMutableArray *listaDetallesMediciones = [NSMutableArray new];
                        
                        for (NSDictionary *infoDetalleMedion  in listaInfoDetallesMediones) {
                            
                            SFMedicionSensorDetalle *medicionSensorDetalle = [SFMedicionSensorDetalle new];
                            
                            if ([infoDetalleMedion objectForKey:@"nro_renglon"] != [NSNull null]) {
                                medicionSensorDetalle.nroRenglon = [[infoDetalleMedion objectForKey:@"nro_renglon"] integerValue];
                            }
                            if ([infoDetalleMedion objectForKey:@"valor"] != [NSNull null]) {
                                medicionSensorDetalle.valorMedicion = [[infoDetalleMedion objectForKey:@"valor"] floatValue];
                            }
                            
                            if ([infoDetalleMedion objectForKey:@"tipo_medicion"] != [NSNull null]) {
                                medicionSensorDetalle.nombreTipoMedicion = [infoDetalleMedion objectForKey:@"tipo_medicion"];
                            }
    
                            [listaDetallesMediciones addObject:medicionSensorDetalle];
                        }
                        
                        ultimaMedicion.listaDetallesMedicion = [NSArray arrayWithArray:listaDetallesMediciones];
                    }
                    respuesta.ultimaMedicion = ultimaMedicion;
                }
                
                if ([datosOperacion objectForKey:@"ejecucion_riego"] != [NSNull null]) {
                    NSDictionary *datos = [datosOperacion objectForKey:@"ejecucion_riego"];
                    
                    SFEjecucionRiego *ejecucionRiego = [SFEjecucionRiego new];
                    
                    if ([datos objectForKey:@"mecanismoRiegoFincaSector"] != [NSNull null]) {
                        ejecucionRiego.idMecanismoRiegoFincaSector = [[datos objectForKey:@"mecanismoRiegoFincaSector"] longLongValue];
                    }
                    if ([datos objectForKey:@"configuracion_riego"] != [NSNull null]) {
                        ejecucionRiego.idConfiguracionRiego = [[datos objectForKey:@"configuracion_riego"] longLongValue];
                    }
                    
                    if ([datos objectForKey:@"estado_ejecucion_riego"] != [NSNull null]) {
                        ejecucionRiego.nombreEstadoEjecucionRiego = [datos objectForKey:@"estado_ejecucion_riego"];
                    }
                    if ([datos objectForKey:@"detalle"] != [NSNull null]) {
                        ejecucionRiego.detalle = [datos objectForKey:@"detalle"];
                    }
                    
                    if ([datos objectForKey:@"cantidadAguaUtilizadaLitros"] != [NSNull null]) {
                        ejecucionRiego.cantidadAguaUtilizadaLitros = [[datos objectForKey:@"cantidadAguaUtilizadaLitros"] floatValue];
                    }
                    
                    if ([datos objectForKey:@"duracionActualMinutos"] != [NSNull null]) {
                        ejecucionRiego.duracionActualMinutos = [[datos objectForKey:@"duracionActualMinutos"] floatValue];
                    }
                    if ([datos objectForKey:@"duracionActualSegundos"] != [NSNull null]) {
                        ejecucionRiego.duracionActualSegundos = [[datos objectForKey:@"duracionActualSegundos"] floatValue];
                    }
                    
                    if ([datos objectForKey:@"fechaHoraFinalizacion"]!= [NSNull null]) {
                        ejecucionRiego.fechaHoraFinalizacion = [SFUtils dateFromStringYYYYMMDDWithTime:datos[@"fechaHoraFinalizacion"]];
                    }
                    if ([datos objectForKey:@""]!= [NSNull null]) {
                        ejecucionRiego.fechaHoraFinalProgramada = [SFUtils dateFromStringYYYYMMDDWithTime:datos[@"fechaHoraFinalProgramada"]];
                    }
                    
                    if ([datos objectForKey:@"fechaHoraInicio"]!= [NSNull null]) {
                        ejecucionRiego.fechaHoraInicio = [SFUtils dateFromStringYYYYMMDDWithTime:datos[@"fechaHoraInicio"]];
                    }
                    if ([datos objectForKey:@"fechaHoraInicio"]!= [NSNull null]) {
                        ejecucionRiego.fechaHoraInicioProgramada = [SFUtils dateFromStringYYYYMMDDWithTime:datos[@"fechaHoraInicioProgramada"]];
                    }
                    
                    respuesta.ejecucionRiego = ejecucionRiego;
                }
                
                if ([datosOperacion objectForKey:@"configuracion_riego"] != [NSNull null]) {
                    NSDictionary *datos = [datosOperacion objectForKey:@"configuracion_riego"];
                    
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
                        configuracionRiego.fechaCreacion = [SFUtils dateFromStringYYYYMMDDWithTime:datos[@"fechaCreacion"]];
                    }
                    if ([datos objectForKey:@"fechaFinalizacion"]!= [NSNull null]) {
                        configuracionRiego.fechaFinalizacion = [SFUtils dateFromStringYYYYMMDDWithTime:datos[@"fechaFinalizacion"]];
                    }
                    
                    if ([datos objectForKey:@"tipoConfiguracionRiego"] != [NSNull null]) {
                        configuracionRiego.nombreTipoConfiguracionRiego = [datos objectForKey:@"tipoConfiguracionRiego"];
                    }
                    if ([datos objectForKey:@"estado_configuracion"] != [NSNull null]) {
                        configuracionRiego.nombreEstadoConfiguracionRiego = [datos objectForKey:@"estado_configuracion"];
                    }
                    
                    if ([datos objectForKey:@"fechaHoraInicio"]!= [NSNull null]) {
                        configuracionRiego.fechaHoraInicio = [SFUtils dateFromStringYYYYMMDDWithTime:datos[@"fechaHoraInicio"]];
                    }
                    if ([datos objectForKey:@"fechaHoraInicioProgramada"]!= [NSNull null]) {
                        configuracionRiego.fechaHoraInicioProgramada = [SFUtils dateFromStringYYYYMMDDWithTime:datos[@"fechaHoraInicioProgramada"]];
                    }

                    respuesta.configuracionRiego = configuracionRiego;
                }
                
            } @catch (NSException *exception) {
                completionBlock(respuesta);
            }
        }
        completionBlock(respuesta);
        
    } failureBlock:^(NSError *error) {
        failureBlock([BaseServicios armarErrorServicio:error]);
    }];
}

+(void) obtenerInformeHistoricoSector:(SolicitudObtenerInformeHistoricoSector*)solicitudObtenerInformeHistoricoSector completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock {
    
    NSMutableDictionary *parametrosLlamada = [NSMutableDictionary new];
    if (solicitudObtenerInformeHistoricoSector) {
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudObtenerInformeHistoricoSector.idFinca] forKey:KEY_ID_FINCA];
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudObtenerInformeHistoricoSector.idSector] forKey:KEY_ID_SECTOR];
        
        [parametrosLlamada setObject:[SFUtils formatDateYYYYMMDD: solicitudObtenerInformeHistoricoSector.fechaInicioSector] forKey:KEY_FECHA_INICIO_SECTOR];
        [parametrosLlamada setObject:[SFUtils formatDateYYYYMMDD: solicitudObtenerInformeHistoricoSector.fechaFinSector] forKey:KEY_FECHA_FIN_SECTOR];
    }
    
    [[HTTPConector instance] httpOperation:OPERATION_OBTENER_INFORME_HISTORICO_SECTOR method:METHOD_POST withParameters:parametrosLlamada completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaObtenerInformeHistoricoSector *respuesta = [RespuestaObtenerInformeHistoricoSector new];
        
        NSDictionary *datosOperacion = [ServiciosModuloReportes armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        if (respuesta.resultado && datosOperacion) {
            
            @try {
                
                if ([datosOperacion objectForKey:@"componenteMedicionListaMediciones"]!= [NSNull null]) {
                    
                    NSDictionary *listaInfoDTOComponenteMedicion = [datosOperacion objectForKey:@"componenteMedicionListaMediciones"];
                    
                    NSMutableArray *listaInstanciasDTOComponenteMedicion = [NSMutableArray new];
                    
                    for (NSDictionary *infoDTOComponenteMedicion in listaInfoDTOComponenteMedicion) {
                        
                        DTOComponenteMedicion *instanciaDTOComponenteMedicion = [DTOComponenteMedicion new];
                        
                        if ([infoDTOComponenteMedicion objectForKey:@"componente"]!= [NSNull null]){
                            NSDictionary *infoComponenteSensor = [infoDTOComponenteMedicion objectForKey:@"componente"];
                            
                            SFComponenteSensor *componenteSensor = [SFComponenteSensor new];
                            
                            if ([infoComponenteSensor objectForKey:@"idComponenteSensor"] != [NSNull null]) {
                                componenteSensor.idComponenteSensor = [[infoComponenteSensor objectForKey:@"idComponenteSensor"] longLongValue];
                            }
                            
                            if ([infoComponenteSensor objectForKey:@"finca"] != [NSNull null]) {
                                componenteSensor.idFinca = [[infoComponenteSensor objectForKey:@"finca"] longLongValue];
                            }
                            
                            if ([infoComponenteSensor objectForKey:@"modelo"] != [NSNull null]) {
                                componenteSensor.modelo = [infoComponenteSensor objectForKey:@"modelo"];
                            }
                            if ([infoComponenteSensor objectForKey:@"descripcion"] != [NSNull null]) {
                                componenteSensor.descripcion = [infoComponenteSensor objectForKey:@"descripcion"];
                            }
                            
                            if ([infoComponenteSensor objectForKey:@"estado"] != [NSNull null]) {
                                componenteSensor.estadoComponenteSensor = [infoComponenteSensor objectForKey:@"estado"];
                            }
                            
                            if ([infoComponenteSensor objectForKey:@"cantidadMaximaSensores"] != [NSNull null]) {
                                componenteSensor.cantidadMaximaSensores = [[infoComponenteSensor objectForKey:@"cantidadMaximaSensores"] integerValue];
                            }
                            if ([infoComponenteSensor objectForKey:@"cantidadSensoresAsignados"] != [NSNull null]) {
                                componenteSensor.cantidadSensoresAsignados = [[infoComponenteSensor objectForKey:@"cantidadSensoresAsignados"] integerValue];
                            }
                            
                            instanciaDTOComponenteMedicion.componenteSensor = componenteSensor;
                        }
                        
                        if ([infoDTOComponenteMedicion objectForKey:@"medicionCabecera"]!= [NSNull null]){
                            NSDictionary *infoMedicionCabecera = [infoDTOComponenteMedicion objectForKey:@"medicionCabecera"];
                            
                            SFMedicionSensorCabecera *medicionCabecera = [SFMedicionSensorCabecera new];
                            
                            if ([infoMedicionCabecera objectForKey:@"nro_medicion"] != [NSNull null]) {
                                medicionCabecera.nroMedicion = [[infoMedicionCabecera objectForKey:@"nro_medicion"] integerValue];
                            }
                            
                            if ([infoMedicionCabecera objectForKey:@"fecha_y_hora"]!= [NSNull null]) {
                                medicionCabecera.fechaYHora = [SFUtils dateFromStringYYYYMMDDWithTime: infoMedicionCabecera[@"fecha_y_hora"]];
                            }
                            
                            if ([infoMedicionCabecera objectForKey:@"lista_mediciones_detalle"]!= [NSNull null]) {
                                NSDictionary *listaInfoDetallesMediones = [infoMedicionCabecera objectForKey:@"lista_mediciones_detalle"];
                                
                                NSMutableArray *listaDetallesMediciones = [NSMutableArray new];
                                
                                for (NSDictionary *infoDetalleMedion  in listaInfoDetallesMediones) {
                                    
                                    SFMedicionSensorDetalle *medicionSensorDetalle = [SFMedicionSensorDetalle new];
                                    
                                    if ([infoDetalleMedion objectForKey:@"nro_renglon"] != [NSNull null]) {
                                        medicionSensorDetalle.nroRenglon = [[infoDetalleMedion objectForKey:@"nro_renglon"] integerValue];
                                    }
                                    if ([infoDetalleMedion objectForKey:@"valor"] != [NSNull null]) {
                                        medicionSensorDetalle.valorMedicion = [[infoDetalleMedion objectForKey:@"valor"] floatValue];
                                    }
                                    
                                    if ([infoDetalleMedion objectForKey:@"tipo_medicion"] != [NSNull null]) {
                                        medicionSensorDetalle.nombreTipoMedicion = [infoDetalleMedion objectForKey:@"tipo_medicion"];
                                    }
                                    
                                    [listaDetallesMediciones addObject:medicionSensorDetalle];
                                }
                                medicionCabecera.listaDetallesMedicion = [NSArray arrayWithArray:listaDetallesMediciones];
                            }
                            instanciaDTOComponenteMedicion.medicionCabecera = medicionCabecera;
                        }
                        
                        [listaInstanciasDTOComponenteMedicion addObject:instanciaDTOComponenteMedicion];
                    }
                    respuesta.listaComponenteMediciones = [NSArray arrayWithArray:listaInstanciasDTOComponenteMedicion];
                }
                
                if ([datosOperacion objectForKey:@"medicionClimaticaList"]!= [NSNull null]) {
                    
                    NSDictionary *listaInfoDTOMedicionClimatica = [datosOperacion objectForKey:@"medicionClimaticaList"];
                    
                    NSMutableArray *listaInstanciasDTOMedicionClimatica = [NSMutableArray new];
                    
                    for (NSDictionary *infoDTOMedicionClimatica in listaInfoDTOMedicionClimatica) {
                        
                        DTOMedicionClimatica *instanciaDTOMedicionClimatica = [DTOMedicionClimatica new];
                        
                        if ([infoDTOMedicionClimatica objectForKey:@"medicionClimatica"]!= [NSNull null]) {
                            NSDictionary *infoMedicionClimaticaCabecera = [infoDTOMedicionClimatica objectForKey:@"medicionClimatica"];
                            
                            SFMedicionInformacionClimaticaCabecera *medicionInformacionClimaticaCabecera = [SFMedicionInformacionClimaticaCabecera new];
                            
                            if ([infoMedicionClimaticaCabecera objectForKey:@"nroMedicion"] != [NSNull null]) {
                                medicionInformacionClimaticaCabecera.nroMedicion = [[infoMedicionClimaticaCabecera objectForKey:@"nroMedicion"] integerValue];
                            }
                            if ([infoMedicionClimaticaCabecera objectForKey:@"fechaHora"]!= [NSNull null]) {
                                medicionInformacionClimaticaCabecera.fechaYHora = [SFUtils dateFromStringYYYYMMDDWithTime: infoMedicionClimaticaCabecera[@"fechaHora"]];
                            }
                            if ([infoMedicionClimaticaCabecera objectForKey:@"proveedorInformacion"] != [NSNull null]) {
                                medicionInformacionClimaticaCabecera.nombreProveedor = [infoMedicionClimaticaCabecera objectForKey:@"proveedorInformacion"];
                            }
                       
                            if ([infoMedicionClimaticaCabecera objectForKey:@"mediciones_detalles"] != [NSNull null]) {
                                NSDictionary *listaInfoDetallesMedicionClimatica = [infoMedicionClimaticaCabecera objectForKey:@"mediciones_detalles"];
                                
                                NSMutableArray *listaInstanciasDetalleMedicionClimatica = [NSMutableArray new];
                                
                                for (NSDictionary *infoDetalleMedicionClimatica in listaInfoDetallesMedicionClimatica) {
                                    
                                    SFMedicionInformacionClimaticaDetalle *medicionInformacionClimaticaDetalle = [SFMedicionInformacionClimaticaDetalle new];
                                    
                                    if ([infoDetalleMedicionClimatica objectForKey:@"nroRenglon"] != [NSNull null]) {
                                        medicionInformacionClimaticaDetalle.nroRenglon = [[infoDetalleMedicionClimatica objectForKey:@"nroRenglon"] integerValue];
                                    }
                                    if ([infoDetalleMedicionClimatica objectForKey:@"valor"] != [NSNull null]) {
                                        medicionInformacionClimaticaDetalle.valorMedicion = [[infoDetalleMedicionClimatica objectForKey:@"valor"] floatValue];
                                    }
                                    
                                    if ([infoDetalleMedicionClimatica objectForKey:@"tipoMedicionClimatica"] != [NSNull null]) {
                                        medicionInformacionClimaticaDetalle.nombreTipoMedicion = [infoDetalleMedicionClimatica objectForKey:@"tipoMedicionClimatica"];
                                    }
                                    [listaInstanciasDetalleMedicionClimatica addObject:medicionInformacionClimaticaDetalle];
                                }
                                
                                medicionInformacionClimaticaCabecera.listaDetallesMedicionInformacionClimatica = [NSArray arrayWithArray:listaInstanciasDetalleMedicionClimatica];
                            }
                            instanciaDTOMedicionClimatica.medicionInformacionClimaticaCabecera = medicionInformacionClimaticaCabecera;
                        }
                        
                        [listaInstanciasDTOMedicionClimatica addObject:instanciaDTOMedicionClimatica];
                    }
                    respuesta.listaMedicionesClimaticas = [NSArray arrayWithArray:listaInstanciasDTOMedicionClimatica];
                }
                
            } @catch (NSException *exception) {
                completionBlock(respuesta);
            }
        }
        completionBlock(respuesta);
        
    } failureBlock:^(NSError *error) {
        failureBlock([BaseServicios armarErrorServicio:error]);
    }];
    
}

+(void) obtenerInformeRiegoEjecucionSector:(SolicitudObtenerInformeRiegoEjecucionSector*)solicitudObtenerInformeRiegoEjecucionSector completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock {
    
    NSMutableDictionary *parametrosLlamada = [NSMutableDictionary new];
    if (solicitudObtenerInformeRiegoEjecucionSector) {
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudObtenerInformeRiegoEjecucionSector.idFinca] forKey:KEY_ID_FINCA];
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudObtenerInformeRiegoEjecucionSector.idSector] forKey:KEY_ID_SECTOR];
    }
    
    [[HTTPConector instance] httpOperation:OPERATION_OBTENER_INFORME_RIEGO_EJECUCION_SECTOR method:METHOD_POST withParameters:parametrosLlamada completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaObtenerInformeRiegoEjecucionSector *respuesta = [RespuestaObtenerInformeRiegoEjecucionSector new];
        
        NSDictionary *datosOperacion = [ServiciosModuloReportes armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        if (respuesta.resultado && datosOperacion) {
            
            @try {
                
                if ([datosOperacion objectForKey:@"id_sector"] != [NSNull null]) {
                    respuesta.idSector = [[datosOperacion objectForKey:@"id_sector"] longLongValue];
                }
                
                if ([datosOperacion objectForKey:@"numero_sector"] != [NSNull null]) {
                    respuesta.nroSector = [[datosOperacion objectForKey:@"numero_sector"] integerValue];
                }
                
                if ([datosOperacion objectForKey:@"mecanismo_sector"] != [NSNull null]) {
                    NSDictionary *infoMecanismoSector = [datosOperacion objectForKey:@"mecanismo_sector"];
                    
                    SFMecanismoRiegoFincaSector *mecanismoRiegoFincaSector = [SFMecanismoRiegoFincaSector new];
                    
                    if ([infoMecanismoSector objectForKey:KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR] != [NSNull null]) {
                        mecanismoRiegoFincaSector.idMecanismoRiegoFincaSector = [[infoMecanismoSector objectForKey:KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR] longLongValue];
                    }
                    
                    if ([infoMecanismoSector objectForKey:KEY_ID_FINCA] != [NSNull null]) {
                        mecanismoRiegoFincaSector.idFinca = [[infoMecanismoSector objectForKey:KEY_ID_FINCA] longLongValue];
                    }
                    if ([infoMecanismoSector objectForKey:KEY_ID_MECANISMO_RIEGO_FINCA] != [NSNull null]) {
                        mecanismoRiegoFincaSector.idMecanismoRiegoFinca = [[infoMecanismoSector objectForKey:KEY_ID_MECANISMO_RIEGO_FINCA] longLongValue];
                    }
                    if ([infoMecanismoSector objectForKey:KEY_ID_SECTOR] != [NSNull null]) {
                        mecanismoRiegoFincaSector.idSector = [[infoMecanismoSector objectForKey:KEY_ID_SECTOR] longLongValue];
                    }
                    
                    if ([infoMecanismoSector objectForKey:KEY_NOMBRE_TIPO_MECANISMO] != [NSNull null]) {
                        mecanismoRiegoFincaSector.nombreTipoMecanismo = [infoMecanismoSector objectForKey:KEY_NOMBRE_TIPO_MECANISMO];
                    }
                    
                    if ([infoMecanismoSector objectForKey:KEY_MECANISMO_RIEGO_CAUDAL_RESPUESTA] != [NSNull null]) {
                        mecanismoRiegoFincaSector.caudal = [[infoMecanismoSector objectForKey:KEY_MECANISMO_RIEGO_CAUDAL_RESPUESTA] floatValue];
                    }
                    if ([infoMecanismoSector objectForKey:KEY_MECANISMO_RIEGO_PRESION_RESPUESTA] != [NSNull null]) {
                        mecanismoRiegoFincaSector.presion = [[infoMecanismoSector objectForKey:KEY_MECANISMO_RIEGO_PRESION_RESPUESTA] floatValue];
                    }
                    
                    respuesta.mecanismoRiegoFincaSector = mecanismoRiegoFincaSector;
                }

                if ([datosOperacion objectForKey:@"ejecucion_riego"] != [NSNull null]) {
                    NSDictionary *infoEjecucionRiego = [datosOperacion objectForKey:@"ejecucion_riego"];
                    
                    SFEjecucionRiego *ejecucionRiego = [SFEjecucionRiego new];
                    
                    if ([infoEjecucionRiego objectForKey:@"mecanismoRiegoFincaSector"] != [NSNull null]) {
                        ejecucionRiego.idMecanismoRiegoFincaSector = [[infoEjecucionRiego objectForKey:@"mecanismoRiegoFincaSector"] longLongValue];
                    }
                    if ([infoEjecucionRiego objectForKey:@"configuracion_riego"] != [NSNull null]) {
                        ejecucionRiego.idConfiguracionRiego = [[infoEjecucionRiego objectForKey:@"configuracion_riego"] longLongValue];
                    }
                    
                    if ([infoEjecucionRiego objectForKey:@"estado_ejecucion_riego"] != [NSNull null]) {
                        ejecucionRiego.nombreEstadoEjecucionRiego = [infoEjecucionRiego objectForKey:@"estado_ejecucion_riego"];
                    }
                    if ([infoEjecucionRiego objectForKey:@"detalle"] != [NSNull null]) {
                        ejecucionRiego.detalle = [infoEjecucionRiego objectForKey:@"detalle"];
                    }
                    
                    if ([infoEjecucionRiego objectForKey:@"cantidadAguaUtilizadaLitros"] != [NSNull null]) {
                        ejecucionRiego.cantidadAguaUtilizadaLitros = [[infoEjecucionRiego objectForKey:@"cantidadAguaUtilizadaLitros"] floatValue];
                    }
                    
                    if ([infoEjecucionRiego objectForKey:@"duracionActualMinutos"] != [NSNull null]) {
                        ejecucionRiego.duracionActualMinutos = [[infoEjecucionRiego objectForKey:@"duracionActualMinutos"] floatValue];
                    }
                    if ([infoEjecucionRiego objectForKey:@"duracionActualSegundos"] != [NSNull null]) {
                        ejecucionRiego.duracionActualSegundos = [[infoEjecucionRiego objectForKey:@"duracionActualSegundos"] floatValue];
                    }
                    
                    if ([infoEjecucionRiego objectForKey:@"fechaHoraFinalizacion"]!= [NSNull null]) {
                        ejecucionRiego.fechaHoraFinalizacion = [SFUtils dateFromStringYYYYMMDDWithTime:infoEjecucionRiego[@"fechaHoraFinalizacion"]];
                    }
                    if ([infoEjecucionRiego objectForKey:@""]!= [NSNull null]) {
                        ejecucionRiego.fechaHoraFinalProgramada = [SFUtils dateFromStringYYYYMMDDWithTime:infoEjecucionRiego[@"fechaHoraFinalProgramada"]];
                    }
                    
                    if ([infoEjecucionRiego objectForKey:@"fechaHoraInicio"]!= [NSNull null]) {
                        ejecucionRiego.fechaHoraInicio = [SFUtils dateFromStringYYYYMMDDWithTime:infoEjecucionRiego[@"fechaHoraInicio"]];
                    }
                    if ([infoEjecucionRiego objectForKey:@"fechaHoraInicio"]!= [NSNull null]) {
                        ejecucionRiego.fechaHoraInicioProgramada = [SFUtils dateFromStringYYYYMMDDWithTime:infoEjecucionRiego[@"fechaHoraInicioProgramada"]];
                    }
                    
                    respuesta.ejecucionRiego = ejecucionRiego;
                }
                    
                if ([datosOperacion objectForKey:@"configuracion_riego"] != [NSNull null]) {
                    NSDictionary *infoConfiguracionRiego = [datosOperacion objectForKey:@"configuracion_riego"];
                    
                    SFConfiguracionRiego *configuracionRiego = [SFConfiguracionRiego new];
                    
                    if ([infoConfiguracionRiego objectForKey:@"idConfiguracionRiego"] != [NSNull null]) {
                        configuracionRiego.idConfiguracionRiego = [[infoConfiguracionRiego objectForKey:@"idConfiguracionRiego"] longLongValue];
                    }
                    if ([infoConfiguracionRiego objectForKey:@"mecanismoRiegoFincaSector"] != [NSNull null]) {
                        configuracionRiego.idMecanismoRiegoFincaSector = [[infoConfiguracionRiego objectForKey:@"mecanismoRiegoFincaSector"] longLongValue];
                    }
                    
                    if ([infoConfiguracionRiego objectForKey:@"nombre"] != [NSNull null]) {
                        configuracionRiego.nombreConfiguracionRiego = [infoConfiguracionRiego objectForKey:@"nombre"];
                    }
                    if ([infoConfiguracionRiego objectForKey:@"descripcion"] != [NSNull null]) {
                        configuracionRiego.descripcionConfiguracionRiego = [infoConfiguracionRiego objectForKey:@"descripcion"];
                    }
                    
                    if ([infoConfiguracionRiego objectForKey:@"duracionMaxima"] != [NSNull null]) {
                        configuracionRiego.duracionMaxima = [[infoConfiguracionRiego objectForKey:@"duracionMaxima"] floatValue];
                    }
                    
                    if ([infoConfiguracionRiego objectForKey:@"fechaCreacion"]!= [NSNull null]) {
                        configuracionRiego.fechaCreacion = [SFUtils dateFromStringYYYYMMDDWithTime:infoConfiguracionRiego[@"fechaCreacion"]];
                    }
                    if ([infoConfiguracionRiego objectForKey:@"fechaFinalizacion"]!= [NSNull null]) {
                        configuracionRiego.fechaFinalizacion = [SFUtils dateFromStringYYYYMMDDWithTime:infoConfiguracionRiego[@"fechaFinalizacion"]];
                    }
                    
                    if ([infoConfiguracionRiego objectForKey:@"tipoConfiguracionRiego"] != [NSNull null]) {
                        configuracionRiego.nombreTipoConfiguracionRiego = [infoConfiguracionRiego objectForKey:@"tipoConfiguracionRiego"];
                    }
                    if ([infoConfiguracionRiego objectForKey:@"estado_configuracion"] != [NSNull null]) {
                        configuracionRiego.nombreEstadoConfiguracionRiego = [infoConfiguracionRiego objectForKey:@"estado_configuracion"];
                    }
                    
                    if ([infoConfiguracionRiego objectForKey:@"fechaHoraInicio"]!= [NSNull null]) {
                        configuracionRiego.fechaHoraInicio = [SFUtils dateFromStringYYYYMMDDWithTime:infoConfiguracionRiego[@"fechaHoraInicio"]];
                    }
                    if ([infoConfiguracionRiego objectForKey:@"fechaHoraInicioProgramada"]!= [NSNull null]) {
                        configuracionRiego.fechaHoraInicioProgramada = [SFUtils dateFromStringYYYYMMDDWithTime:infoConfiguracionRiego[@"fechaHoraInicioProgramada"]];
                    }
                    
                    respuesta.configuracionRiego = configuracionRiego;
                }
            } @catch (NSException *exception) {
                completionBlock(respuesta);
            }
        }
        completionBlock(respuesta);
        
    } failureBlock:^(NSError *error) {
        failureBlock([BaseServicios armarErrorServicio:error]);
    }];
}

+(void) obtenerInformeRiegoHistoricoSector:(SolicitudObtenerInformeRiegoHistoricoSector*)solicitudObtenerInformeRiegoHistoricoSector completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock {
    
    NSMutableDictionary *parametrosLlamada = [NSMutableDictionary new];
    if (solicitudObtenerInformeRiegoHistoricoSector) {
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudObtenerInformeRiegoHistoricoSector.idFinca] forKey:KEY_ID_FINCA];
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudObtenerInformeRiegoHistoricoSector.idSector] forKey:KEY_ID_SECTOR];
        
        [parametrosLlamada setObject:[SFUtils formatDateYYYYMMDD: solicitudObtenerInformeRiegoHistoricoSector.fechaInicioSector] forKey:KEY_FECHA_INICIO_SECTOR];
        [parametrosLlamada setObject:[SFUtils formatDateYYYYMMDD: solicitudObtenerInformeRiegoHistoricoSector.fechaFinSector] forKey:KEY_FECHA_FIN_SECTOR];
    }
    
    [[HTTPConector instance] httpOperation:OPERATION_OBTENER_INFORME_RIEGO_HISTORICO_SECTOR method:METHOD_POST withParameters:parametrosLlamada completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaObtenerInformeRiegoHistoricoSector *respuesta = [RespuestaObtenerInformeRiegoHistoricoSector new];
        
        NSDictionary *datosOperacion = [ServiciosModuloReportes armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        if (respuesta.resultado && datosOperacion) {
            
            @try {

                NSMutableArray *listaInstancias = [NSMutableArray new];
                
                for (NSDictionary *datos in datosOperacion) {
                    
                    DTOMecanismoRiegoConfiguracion *nuevaInstancia = [DTOMecanismoRiegoConfiguracion new];
                    
                    if ([datos objectForKey:@"mecanismo_riego_finca_sector"] != [NSNull null]) {
                        NSDictionary *infoMecanismoSector = [datos objectForKey:@"mecanismo_riego_finca_sector"];
                        
                        SFMecanismoRiegoFincaSector *mecanismoRiegoFincaSector = [SFMecanismoRiegoFincaSector new];
                        
                        if ([infoMecanismoSector objectForKey:KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR] != [NSNull null]) {
                            mecanismoRiegoFincaSector.idMecanismoRiegoFincaSector = [[infoMecanismoSector objectForKey:KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR] longLongValue];
                        }
                        
                        if ([infoMecanismoSector objectForKey:KEY_ID_FINCA] != [NSNull null]) {
                            mecanismoRiegoFincaSector.idFinca = [[infoMecanismoSector objectForKey:KEY_ID_FINCA] longLongValue];
                        }
                        if ([infoMecanismoSector objectForKey:KEY_ID_MECANISMO_RIEGO_FINCA] != [NSNull null]) {
                            mecanismoRiegoFincaSector.idMecanismoRiegoFinca = [[infoMecanismoSector objectForKey:KEY_ID_MECANISMO_RIEGO_FINCA] longLongValue];
                        }
                        if ([infoMecanismoSector objectForKey:KEY_ID_SECTOR] != [NSNull null]) {
                            mecanismoRiegoFincaSector.idSector = [[infoMecanismoSector objectForKey:KEY_ID_SECTOR] longLongValue];
                        }
                        
                        if ([infoMecanismoSector objectForKey:KEY_NOMBRE_TIPO_MECANISMO] != [NSNull null]) {
                            mecanismoRiegoFincaSector.nombreTipoMecanismo = [infoMecanismoSector objectForKey:KEY_NOMBRE_TIPO_MECANISMO];
                        }
                        
                        if ([infoMecanismoSector objectForKey:KEY_MECANISMO_RIEGO_CAUDAL_RESPUESTA] != [NSNull null]) {
                            mecanismoRiegoFincaSector.caudal = [[infoMecanismoSector objectForKey:KEY_MECANISMO_RIEGO_CAUDAL_RESPUESTA] floatValue];
                        }
                        if ([infoMecanismoSector objectForKey:KEY_MECANISMO_RIEGO_PRESION_RESPUESTA] != [NSNull null]) {
                            mecanismoRiegoFincaSector.presion = [[infoMecanismoSector objectForKey:KEY_MECANISMO_RIEGO_PRESION_RESPUESTA] floatValue];
                        }
                        
                        nuevaInstancia.mecanismoRiegoFincaSector = mecanismoRiegoFincaSector;
                    }
                    
                    if ([datos objectForKey:@"ejecucion"] != [NSNull null]) {
                        NSDictionary *infoEjecucionRiego = [datos objectForKey:@"ejecucion"];
                        
                        SFEjecucionRiego *ejecucionRiego = [SFEjecucionRiego new];
                    
                        if ([infoEjecucionRiego objectForKey:@"mecanismoRiegoFincaSector"] != [NSNull null]) {
                            ejecucionRiego.idMecanismoRiegoFincaSector = [[infoEjecucionRiego objectForKey:@"mecanismoRiegoFincaSector"] longLongValue];
                        }
                        if ([infoEjecucionRiego objectForKey:@"configuracion_riego"] != [NSNull null]) {
                            ejecucionRiego.idConfiguracionRiego = [[infoEjecucionRiego objectForKey:@"configuracion_riego"] longLongValue];
                        }
                        
                        if ([infoEjecucionRiego objectForKey:@"estado_ejecucion_riego"] != [NSNull null]) {
                            ejecucionRiego.nombreEstadoEjecucionRiego = [infoEjecucionRiego objectForKey:@"estado_ejecucion_riego"];
                        }
                        if ([infoEjecucionRiego objectForKey:@"detalle"] != [NSNull null]) {
                            ejecucionRiego.detalle = [infoEjecucionRiego objectForKey:@"detalle"];
                        }
                        
                        if ([infoEjecucionRiego objectForKey:@"cantidadAguaUtilizadaLitros"] != [NSNull null]) {
                            ejecucionRiego.cantidadAguaUtilizadaLitros = [[infoEjecucionRiego objectForKey:@"cantidadAguaUtilizadaLitros"] floatValue];
                        }
                        
                        if ([infoEjecucionRiego objectForKey:@"duracionActualMinutos"] != [NSNull null]) {
                            ejecucionRiego.duracionActualMinutos = [[infoEjecucionRiego objectForKey:@"duracionActualMinutos"] floatValue];
                        }
                        if ([infoEjecucionRiego objectForKey:@"duracionActualSegundos"] != [NSNull null]) {
                            ejecucionRiego.duracionActualSegundos = [[infoEjecucionRiego objectForKey:@"duracionActualSegundos"] floatValue];
                        }
                        
                        if ([infoEjecucionRiego objectForKey:@"fechaHoraFinalizacion"]!= [NSNull null]) {
                            ejecucionRiego.fechaHoraFinalizacion = [SFUtils dateFromStringYYYYMMDDWithTime:infoEjecucionRiego[@"fechaHoraFinalizacion"]];
                        }
                        if ([infoEjecucionRiego objectForKey:@""]!= [NSNull null]) {
                            ejecucionRiego.fechaHoraFinalProgramada = [SFUtils dateFromStringYYYYMMDDWithTime:infoEjecucionRiego[@"fechaHoraFinalProgramada"]];
                        }
                        
                        if ([infoEjecucionRiego objectForKey:@"fechaHoraInicio"]!= [NSNull null]) {
                            ejecucionRiego.fechaHoraInicio = [SFUtils dateFromStringYYYYMMDDWithTime:infoEjecucionRiego[@"fechaHoraInicio"]];
                        }
                        if ([infoEjecucionRiego objectForKey:@"fechaHoraInicio"]!= [NSNull null]) {
                            ejecucionRiego.fechaHoraInicioProgramada = [SFUtils dateFromStringYYYYMMDDWithTime:infoEjecucionRiego[@"fechaHoraInicioProgramada"]];
                        }
                        
                        nuevaInstancia.ejecucionRiego = ejecucionRiego;
                    }
                    
                    if ([datos objectForKey:@"configuracion"] != [NSNull null]) {
                        NSDictionary *infoConfiguracionRiego = [datos objectForKey:@"configuracion"];
                        
                        SFConfiguracionRiego *configuracionRiego = [SFConfiguracionRiego new];
                        
                        if ([infoConfiguracionRiego objectForKey:@"idConfiguracionRiego"] != [NSNull null]) {
                            configuracionRiego.idConfiguracionRiego = [[infoConfiguracionRiego objectForKey:@"idConfiguracionRiego"] longLongValue];
                        }
                        if ([infoConfiguracionRiego objectForKey:@"mecanismoRiegoFincaSector"] != [NSNull null]) {
                            configuracionRiego.idMecanismoRiegoFincaSector = [[infoConfiguracionRiego objectForKey:@"mecanismoRiegoFincaSector"] longLongValue];
                        }
                        
                        if ([infoConfiguracionRiego objectForKey:@"nombre"] != [NSNull null]) {
                            configuracionRiego.nombreConfiguracionRiego = [infoConfiguracionRiego objectForKey:@"nombre"];
                        }
                        if ([infoConfiguracionRiego objectForKey:@"descripcion"] != [NSNull null]) {
                            configuracionRiego.descripcionConfiguracionRiego = [infoConfiguracionRiego objectForKey:@"descripcion"];
                        }
                        
                        if ([infoConfiguracionRiego objectForKey:@"duracionMaxima"] != [NSNull null]) {
                            configuracionRiego.duracionMaxima = [[infoConfiguracionRiego objectForKey:@"duracionMaxima"] floatValue];
                        }
                        
                        if ([infoConfiguracionRiego objectForKey:@"fechaCreacion"]!= [NSNull null]) {
                            configuracionRiego.fechaCreacion = [SFUtils dateFromStringYYYYMMDDWithTime:infoConfiguracionRiego[@"fechaCreacion"]];
                        }
                        if ([infoConfiguracionRiego objectForKey:@"fechaFinalizacion"]!= [NSNull null]) {
                            configuracionRiego.fechaFinalizacion = [SFUtils dateFromStringYYYYMMDDWithTime:infoConfiguracionRiego[@"fechaFinalizacion"]];
                        }
                        
                        if ([infoConfiguracionRiego objectForKey:@"tipoConfiguracionRiego"] != [NSNull null]) {
                            configuracionRiego.nombreTipoConfiguracionRiego = [infoConfiguracionRiego objectForKey:@"tipoConfiguracionRiego"];
                        }
                        if ([infoConfiguracionRiego objectForKey:@"estado_configuracion"] != [NSNull null]) {
                            configuracionRiego.nombreEstadoConfiguracionRiego = [infoConfiguracionRiego objectForKey:@"estado_configuracion"];
                        }
                        
                        if ([infoConfiguracionRiego objectForKey:@"fechaHoraInicio"]!= [NSNull null]) {
                            configuracionRiego.fechaHoraInicio = [SFUtils dateFromStringYYYYMMDDWithTime:infoConfiguracionRiego[@"fechaHoraInicio"]];
                        }
                        if ([infoConfiguracionRiego objectForKey:@"fechaHoraInicioProgramada"]!= [NSNull null]) {
                            configuracionRiego.fechaHoraInicioProgramada = [SFUtils dateFromStringYYYYMMDDWithTime:infoConfiguracionRiego[@"fechaHoraInicioProgramada"]];
                        }
                        
                        nuevaInstancia.configuracionRiego = configuracionRiego;
                    }
                    
                    [listaInstancias addObject:nuevaInstancia];
                }
                
                respuesta.listaDTOMecanismoRiegoConfiguracion = [NSArray arrayWithArray:listaInstancias];
                
            } @catch (NSException *exception) {
                completionBlock(respuesta);
            }
        }
        completionBlock(respuesta);
        
    } failureBlock:^(NSError *error) {
        failureBlock([BaseServicios armarErrorServicio:error]);
    }];
    
}

+(void) obtenerInformeEventosPersonalizados:(SolicitudObtenerInformeEventosPersonalizados*)solicitudObtenerInformeEventosPersonalizados completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock {
    
    NSMutableDictionary *parametrosLlamada = [NSMutableDictionary new];
    if (solicitudObtenerInformeEventosPersonalizados) {
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudObtenerInformeEventosPersonalizados.idFinca] forKey:KEY_ID_FINCA];
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudObtenerInformeEventosPersonalizados.idConfiguracionEvento] forKey:KEY_ID_CONFIGURACION_EVENTO_PERSONALIZADO];
    }
    
    [[HTTPConector instance] httpOperation:OPERATION_OBTENER_INFORME_EVENTOS_PERSONALIZADOS method:METHOD_POST withParameters:parametrosLlamada completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaObtenerInformeEventosPersonalizados *respuesta = [RespuestaObtenerInformeEventosPersonalizados new];
        
        NSDictionary *datosOperacion = [ServiciosModuloReportes armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        if (respuesta.resultado && datosOperacion) {
            
            @try {
                
                NSMutableArray *listaInstancias = [NSMutableArray new];
                
                for (NSDictionary *datos in datosOperacion) {
                    
                    SFOcurrenciaEventoPersonalizado *nuevaInstancia = [SFOcurrenciaEventoPersonalizado new];
                    
                    if ([datos objectForKey:@"nroEvento"] != [NSNull null]) {
                        nuevaInstancia.nroEvento = [[datos objectForKey:@"nroEvento"] integerValue];
                    }
                    
                    if ([datos objectForKey:@"numeroSector"] != [NSNull null]) {
                        nuevaInstancia.numeroSector = [[datos objectForKey:@"numeroSector"] integerValue];
                    }
                    
                    if ([datos objectForKey:@"fechaHora"] != [NSNull null]) {
                        nuevaInstancia.fechaYHora = [SFUtils dateFromStringYYYYMMDDWithTime: datos[@"fechaHora"]];
                    }
                    
                    [listaInstancias addObject:nuevaInstancia];
                }
                
                respuesta.listaOcurrenciasEventoPersonalizado = [NSArray arrayWithArray:listaInstancias];
                
            } @catch (NSException *exception) {
                completionBlock(respuesta);
            }
        }
        completionBlock(respuesta);
        
    } failureBlock:^(NSError *error) {
        failureBlock([BaseServicios armarErrorServicio:error]);
    }];
    
}

+(void) obtenerInformeHistoricoHeladas:(SolicitudObtenerInformeHistoricoHeladas*)solicitudObtenerInformeHistoricoHeladas completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock {
    
    NSMutableDictionary *parametrosLlamada = [NSMutableDictionary new];
    if (solicitudObtenerInformeHistoricoHeladas) {
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudObtenerInformeHistoricoHeladas.idFinca] forKey:KEY_ID_FINCA];
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudObtenerInformeHistoricoHeladas.idSector] forKey:KEY_ID_SECTOR];
        
        [parametrosLlamada setObject:[SFUtils formatDateYYYYMMDD: solicitudObtenerInformeHistoricoHeladas.fechaInicioSector] forKey:KEY_FECHA_INICIO_SECTOR];
        [parametrosLlamada setObject:[SFUtils formatDateYYYYMMDD: solicitudObtenerInformeHistoricoHeladas.fechaFinSector] forKey:KEY_FECHA_FIN_SECTOR];
    }
    
    [[HTTPConector instance] httpOperation:OPERATION_OBTENER_INFORME_HISTORICO_HELADAS method:METHOD_POST withParameters:parametrosLlamada completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaObtenerInformeHistoricoHeladas *respuesta = [RespuestaObtenerInformeHistoricoHeladas new];
        
        NSDictionary *datosOperacion = [ServiciosModuloReportes armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        if (respuesta.resultado && datosOperacion) {
            
            @try {
                
                NSMutableArray *listaInstancias = [NSMutableArray new];
                
                for (NSDictionary *datos in datosOperacion) {
                    
                    SFOcurrenciaEventoPersonalizado *nuevaInstancia = [SFOcurrenciaEventoPersonalizado new];
                    
                    if ([datos objectForKey:@"nroEvento"] != [NSNull null]) {
                        nuevaInstancia.nroEvento = [[datos objectForKey:@"nroEvento"] integerValue];
                    }
                    
                    if ([datos objectForKey:@"numeroSector"] != [NSNull null]) {
                        nuevaInstancia.numeroSector = [[datos objectForKey:@"numeroSector"] integerValue];
                    }
                    
                    if ([datos objectForKey:@"fechaHora"] != [NSNull null]) {
                        nuevaInstancia.fechaYHora = [SFUtils dateFromStringYYYYMMDDWithTime: datos[@"fechaHora"]];
                    }
                    
                    [listaInstancias addObject:nuevaInstancia];
                }
                
                respuesta.listaOcurrenciasHelada = [NSArray arrayWithArray:listaInstancias];
                
            } @catch (NSException *exception) {
                completionBlock(respuesta);
            }
        }
        completionBlock(respuesta);
        
    } failureBlock:^(NSError *error) {
        failureBlock([BaseServicios armarErrorServicio:error]);
    }];
    
}

+(void) obtenerInformeCruzadoRiegoMediciones:(SolicitudObtenerInformeCruzadoRiegoMediciones*)solicitudObtenerInformeCruzadoRiegoMediciones completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock {
    
    NSMutableDictionary *parametrosLlamada = [NSMutableDictionary new];
    if (solicitudObtenerInformeCruzadoRiegoMediciones) {
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudObtenerInformeCruzadoRiegoMediciones.idFinca] forKey:KEY_ID_FINCA];
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudObtenerInformeCruzadoRiegoMediciones.idSector] forKey:KEY_ID_SECTOR];
        
        [parametrosLlamada setObject:[SFUtils formatDateYYYYMMDD: solicitudObtenerInformeCruzadoRiegoMediciones.fechaInicioSector] forKey:KEY_FECHA_INICIO_SECTOR];
        [parametrosLlamada setObject:[SFUtils formatDateYYYYMMDD: solicitudObtenerInformeCruzadoRiegoMediciones.fechaFinSector] forKey:KEY_FECHA_FIN_SECTOR];
    }
    
    [[HTTPConector instance] httpOperation:OPERATION_OBTENER_INFORME_CRUZADO_RIEGO_MEDICIONES method:METHOD_POST withParameters:parametrosLlamada completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaObtenerInformeCruzadoRiegoMediciones *respuesta = [RespuestaObtenerInformeCruzadoRiegoMediciones new];
        
        NSDictionary *datosOperacion = [ServiciosModuloReportes armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        if (respuesta.resultado && datosOperacion) {
            
            @try {
                
                NSMutableArray *listaInstancias = [NSMutableArray new];
                
                for (NSDictionary *datos in datosOperacion) {
                    
                    DTOInformeCruzadoRiegoMediciones *nuevaInstancia = [DTOInformeCruzadoRiegoMediciones new];
                    
                    if ([datos objectForKey:@"mecanismo_riego_finca_sector"] != [NSNull null]) {
                        NSDictionary *infoMecanismoSector = [datos objectForKey:@"mecanismo_riego_finca_sector"];
                        
                        SFMecanismoRiegoFincaSector *mecanismoRiegoFincaSector = [SFMecanismoRiegoFincaSector new];
                        
                        if ([infoMecanismoSector objectForKey:KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR] != [NSNull null]) {
                            mecanismoRiegoFincaSector.idMecanismoRiegoFincaSector = [[infoMecanismoSector objectForKey:KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR] longLongValue];
                        }
                        
                        if ([infoMecanismoSector objectForKey:KEY_ID_FINCA] != [NSNull null]) {
                            mecanismoRiegoFincaSector.idFinca = [[infoMecanismoSector objectForKey:KEY_ID_FINCA] longLongValue];
                        }
                        if ([infoMecanismoSector objectForKey:KEY_ID_MECANISMO_RIEGO_FINCA] != [NSNull null]) {
                            mecanismoRiegoFincaSector.idMecanismoRiegoFinca = [[infoMecanismoSector objectForKey:KEY_ID_MECANISMO_RIEGO_FINCA] longLongValue];
                        }
                        if ([infoMecanismoSector objectForKey:KEY_ID_SECTOR] != [NSNull null]) {
                            mecanismoRiegoFincaSector.idSector = [[infoMecanismoSector objectForKey:KEY_ID_SECTOR] longLongValue];
                        }
                        
                        if ([infoMecanismoSector objectForKey:KEY_NOMBRE_TIPO_MECANISMO] != [NSNull null]) {
                            mecanismoRiegoFincaSector.nombreTipoMecanismo = [infoMecanismoSector objectForKey:KEY_NOMBRE_TIPO_MECANISMO];
                        }
                        
                        if ([infoMecanismoSector objectForKey:KEY_MECANISMO_RIEGO_CAUDAL_RESPUESTA] != [NSNull null]) {
                            mecanismoRiegoFincaSector.caudal = [[infoMecanismoSector objectForKey:KEY_MECANISMO_RIEGO_CAUDAL_RESPUESTA] floatValue];
                        }
                        if ([infoMecanismoSector objectForKey:KEY_MECANISMO_RIEGO_PRESION_RESPUESTA] != [NSNull null]) {
                            mecanismoRiegoFincaSector.presion = [[infoMecanismoSector objectForKey:KEY_MECANISMO_RIEGO_PRESION_RESPUESTA] floatValue];
                        }
                        
                        nuevaInstancia.mecanismoRiegoFincaSector = mecanismoRiegoFincaSector;
                    }
                    
                    if ([datos objectForKey:@"ejecucion"] != [NSNull null]) {
                        NSDictionary *infoEjecucionRiego = [datos objectForKey:@"ejecucion"];
                        
                        SFEjecucionRiego *ejecucionRiego = [SFEjecucionRiego new];
                        
                        if ([infoEjecucionRiego objectForKey:@"mecanismoRiegoFincaSector"] != [NSNull null]) {
                            ejecucionRiego.idMecanismoRiegoFincaSector = [[infoEjecucionRiego objectForKey:@"mecanismoRiegoFincaSector"] longLongValue];
                        }
                        if ([infoEjecucionRiego objectForKey:@"configuracion_riego"] != [NSNull null]) {
                            ejecucionRiego.idConfiguracionRiego = [[infoEjecucionRiego objectForKey:@"configuracion_riego"] longLongValue];
                        }
                        
                        if ([infoEjecucionRiego objectForKey:@"estado_ejecucion_riego"] != [NSNull null]) {
                            ejecucionRiego.nombreEstadoEjecucionRiego = [infoEjecucionRiego objectForKey:@"estado_ejecucion_riego"];
                        }
                        if ([infoEjecucionRiego objectForKey:@"detalle"] != [NSNull null]) {
                            ejecucionRiego.detalle = [infoEjecucionRiego objectForKey:@"detalle"];
                        }
                        
                        if ([infoEjecucionRiego objectForKey:@"cantidadAguaUtilizadaLitros"] != [NSNull null]) {
                            ejecucionRiego.cantidadAguaUtilizadaLitros = [[infoEjecucionRiego objectForKey:@"cantidadAguaUtilizadaLitros"] floatValue];
                        }
                        
                        if ([infoEjecucionRiego objectForKey:@"duracionActualMinutos"] != [NSNull null]) {
                            ejecucionRiego.duracionActualMinutos = [[infoEjecucionRiego objectForKey:@"duracionActualMinutos"] floatValue];
                        }
                        if ([infoEjecucionRiego objectForKey:@"duracionActualSegundos"] != [NSNull null]) {
                            ejecucionRiego.duracionActualSegundos = [[infoEjecucionRiego objectForKey:@"duracionActualSegundos"] floatValue];
                        }
                        
                        if ([infoEjecucionRiego objectForKey:@"fechaHoraFinalizacion"]!= [NSNull null]) {
                            ejecucionRiego.fechaHoraFinalizacion = [SFUtils dateFromStringYYYYMMDDWithTime:infoEjecucionRiego[@"fechaHoraFinalizacion"]];
                        }
                        if ([infoEjecucionRiego objectForKey:@""]!= [NSNull null]) {
                            ejecucionRiego.fechaHoraFinalProgramada = [SFUtils dateFromStringYYYYMMDDWithTime:infoEjecucionRiego[@"fechaHoraFinalProgramada"]];
                        }
                        
                        if ([infoEjecucionRiego objectForKey:@"fechaHoraInicio"]!= [NSNull null]) {
                            ejecucionRiego.fechaHoraInicio = [SFUtils dateFromStringYYYYMMDDWithTime:infoEjecucionRiego[@"fechaHoraInicio"]];
                        }
                        if ([infoEjecucionRiego objectForKey:@"fechaHoraInicio"]!= [NSNull null]) {
                            ejecucionRiego.fechaHoraInicioProgramada = [SFUtils dateFromStringYYYYMMDDWithTime:infoEjecucionRiego[@"fechaHoraInicioProgramada"]];
                        }
                        
                        nuevaInstancia.ejecucionRiego = ejecucionRiego;
                    }
                    
                    if ([datos objectForKey:@"configuracion"] != [NSNull null]) {
                        NSDictionary *infoConfiguracionRiego = [datos objectForKey:@"configuracion"];
                        
                        SFConfiguracionRiego *configuracionRiego = [SFConfiguracionRiego new];
                        
                        if ([infoConfiguracionRiego objectForKey:@"idConfiguracionRiego"] != [NSNull null]) {
                            configuracionRiego.idConfiguracionRiego = [[infoConfiguracionRiego objectForKey:@"idConfiguracionRiego"] longLongValue];
                        }
                        if ([infoConfiguracionRiego objectForKey:@"mecanismoRiegoFincaSector"] != [NSNull null]) {
                            configuracionRiego.idMecanismoRiegoFincaSector = [[infoConfiguracionRiego objectForKey:@"mecanismoRiegoFincaSector"] longLongValue];
                        }
                        
                        if ([infoConfiguracionRiego objectForKey:@"nombre"] != [NSNull null]) {
                            configuracionRiego.nombreConfiguracionRiego = [infoConfiguracionRiego objectForKey:@"nombre"];
                        }
                        if ([infoConfiguracionRiego objectForKey:@"descripcion"] != [NSNull null]) {
                            configuracionRiego.descripcionConfiguracionRiego = [infoConfiguracionRiego objectForKey:@"descripcion"];
                        }
                        
                        if ([infoConfiguracionRiego objectForKey:@"duracionMaxima"] != [NSNull null]) {
                            configuracionRiego.duracionMaxima = [[infoConfiguracionRiego objectForKey:@"duracionMaxima"] floatValue];
                        }
                        
                        if ([infoConfiguracionRiego objectForKey:@"fechaCreacion"]!= [NSNull null]) {
                            configuracionRiego.fechaCreacion = [SFUtils dateFromStringYYYYMMDDWithTime:infoConfiguracionRiego[@"fechaCreacion"]];
                        }
                        if ([infoConfiguracionRiego objectForKey:@"fechaFinalizacion"]!= [NSNull null]) {
                            configuracionRiego.fechaFinalizacion = [SFUtils dateFromStringYYYYMMDDWithTime:infoConfiguracionRiego[@"fechaFinalizacion"]];
                        }
                        
                        if ([infoConfiguracionRiego objectForKey:@"tipoConfiguracionRiego"] != [NSNull null]) {
                            configuracionRiego.nombreTipoConfiguracionRiego = [infoConfiguracionRiego objectForKey:@"tipoConfiguracionRiego"];
                        }
                        if ([infoConfiguracionRiego objectForKey:@"estado_configuracion"] != [NSNull null]) {
                            configuracionRiego.nombreEstadoConfiguracionRiego = [infoConfiguracionRiego objectForKey:@"estado_configuracion"];
                        }
                        
                        if ([infoConfiguracionRiego objectForKey:@"fechaHoraInicio"]!= [NSNull null]) {
                            configuracionRiego.fechaHoraInicio = [SFUtils dateFromStringYYYYMMDDWithTime:infoConfiguracionRiego[@"fechaHoraInicio"]];
                        }
                        if ([infoConfiguracionRiego objectForKey:@"fechaHoraInicioProgramada"]!= [NSNull null]) {
                            configuracionRiego.fechaHoraInicioProgramada = [SFUtils dateFromStringYYYYMMDDWithTime:infoConfiguracionRiego[@"fechaHoraInicioProgramada"]];
                        }
 
                        nuevaInstancia.configuracionRiego = configuracionRiego;
                    }

                    if ([datos objectForKey:@"medicionesComponenteAntes"] != [NSNull null]) {
                        NSDictionary *listaInfoMedicionesComponenteAntes = [datos objectForKey:@"medicionesComponenteAntes"];
                        
                        NSMutableArray *listaMedicionesComponenteAntes = [NSMutableArray new];
                        
                        for (NSDictionary *infoMedicionCabecera in listaInfoMedicionesComponenteAntes) {
                            
                            SFMedicionSensorCabecera *medicionCabecera = [SFMedicionSensorCabecera new];
                            
                            if ([infoMedicionCabecera objectForKey:@"nro_medicion"] != [NSNull null]) {
                                medicionCabecera.nroMedicion = [[infoMedicionCabecera objectForKey:@"nro_medicion"] integerValue];
                            }
                            
                            if ([infoMedicionCabecera objectForKey:@"fecha_y_hora"]!= [NSNull null]) {
                                medicionCabecera.fechaYHora = [SFUtils dateFromStringYYYYMMDDWithTime: infoMedicionCabecera[@"fecha_y_hora"]];
                            }
                            
                            if ([infoMedicionCabecera objectForKey:@"lista_mediciones_detalle"]!= [NSNull null]) {
                                NSDictionary *listaInfoDetallesMediones = [infoMedicionCabecera objectForKey:@"lista_mediciones_detalle"];
                                
                                NSMutableArray *listaDetallesMediciones = [NSMutableArray new];
                                
                                for (NSDictionary *infoDetalleMedion  in listaInfoDetallesMediones) {
                                    
                                    SFMedicionSensorDetalle *medicionSensorDetalle = [SFMedicionSensorDetalle new];
                                    
                                    if ([infoDetalleMedion objectForKey:@"nro_renglon"] != [NSNull null]) {
                                        medicionSensorDetalle.nroRenglon = [[infoDetalleMedion objectForKey:@"nro_renglon"] integerValue];
                                    }
                                    if ([infoDetalleMedion objectForKey:@"valor"] != [NSNull null]) {
                                        medicionSensorDetalle.valorMedicion = [[infoDetalleMedion objectForKey:@"valor"] floatValue];
                                    }
                                    
                                    if ([infoDetalleMedion objectForKey:@"tipo_medicion"] != [NSNull null]) {
                                        medicionSensorDetalle.nombreTipoMedicion = [infoDetalleMedion objectForKey:@"tipo_medicion"];
                                    }
                                    
                                    [listaDetallesMediciones addObject:medicionSensorDetalle];
                                }
                                medicionCabecera.listaDetallesMedicion = [NSArray arrayWithArray:listaDetallesMediciones];
                            }

                            [listaMedicionesComponenteAntes addObject:medicionCabecera];
                        }
                        nuevaInstancia.medicionesComponenteAntes = [NSArray arrayWithArray:listaMedicionesComponenteAntes];
                    }
                    
                    if ([datos objectForKey:@"medicionesComponenteDespues"] != [NSNull null]) {
                        NSDictionary *listaInfoMedicionesComponenteDespues = [datos objectForKey:@"medicionesComponenteDespues"];
                        
                        NSMutableArray *listaMedicionesComponenteDespues = [NSMutableArray new];
                        
                        for (NSDictionary *infoMedicionCabecera in listaInfoMedicionesComponenteDespues) {
                            
                            SFMedicionSensorCabecera *medicionCabecera = [SFMedicionSensorCabecera new];
                            
                            if ([infoMedicionCabecera objectForKey:@"nro_medicion"] != [NSNull null]) {
                                medicionCabecera.nroMedicion = [[infoMedicionCabecera objectForKey:@"nro_medicion"] integerValue];
                            }
                            
                            if ([infoMedicionCabecera objectForKey:@"fecha_y_hora"]!= [NSNull null]) {
                                medicionCabecera.fechaYHora = [SFUtils dateFromStringYYYYMMDDWithTime: infoMedicionCabecera[@"fecha_y_hora"]];
                            }
                            
                            if ([infoMedicionCabecera objectForKey:@"lista_mediciones_detalle"]!= [NSNull null]) {
                                NSDictionary *listaInfoDetallesMediones = [infoMedicionCabecera objectForKey:@"lista_mediciones_detalle"];
                                
                                NSMutableArray *listaDetallesMediciones = [NSMutableArray new];
                                
                                for (NSDictionary *infoDetalleMedion  in listaInfoDetallesMediones) {
                                    
                                    SFMedicionSensorDetalle *medicionSensorDetalle = [SFMedicionSensorDetalle new];
                                    
                                    if ([infoDetalleMedion objectForKey:@"nro_renglon"] != [NSNull null]) {
                                        medicionSensorDetalle.nroRenglon = [[infoDetalleMedion objectForKey:@"nro_renglon"] integerValue];
                                    }
                                    if ([infoDetalleMedion objectForKey:@"valor"] != [NSNull null]) {
                                        medicionSensorDetalle.valorMedicion = [[infoDetalleMedion objectForKey:@"valor"] floatValue];
                                    }
                                    
                                    if ([infoDetalleMedion objectForKey:@"tipo_medicion"] != [NSNull null]) {
                                        medicionSensorDetalle.nombreTipoMedicion = [infoDetalleMedion objectForKey:@"tipo_medicion"];
                                    }
                                    
                                    [listaDetallesMediciones addObject:medicionSensorDetalle];
                                }
                                medicionCabecera.listaDetallesMedicion = [NSArray arrayWithArray:listaDetallesMediciones];
                            }
                            
                            [listaMedicionesComponenteDespues addObject:medicionCabecera];
                        }
                        nuevaInstancia.medicionesComponenteDespues = [NSArray arrayWithArray:listaMedicionesComponenteDespues];
                    }
                    
                    if ([datos objectForKey:@"medicionesClimaticasAntes"] != [NSNull null]) {
                        NSDictionary *listaInfoMedicionesClimaticas = [datos objectForKey:@"medicionesClimaticasAntes"];
                        
                        NSMutableArray *listaMedicionesClimaticas = [NSMutableArray new];
                        
                        for (NSDictionary *infoMedicionClimaticaCabecera in listaInfoMedicionesClimaticas) {
                            
                            SFMedicionInformacionClimaticaCabecera *medicionInformacionClimaticaCabecera = [SFMedicionInformacionClimaticaCabecera new];
                            
                            if ([infoMedicionClimaticaCabecera objectForKey:@"nroMedicion"] != [NSNull null]) {
                                medicionInformacionClimaticaCabecera.nroMedicion = [[infoMedicionClimaticaCabecera objectForKey:@"nroMedicion"] integerValue];
                            }
                            if ([infoMedicionClimaticaCabecera objectForKey:@"fechaHora"]!= [NSNull null]) {
                                medicionInformacionClimaticaCabecera.fechaYHora = [SFUtils dateFromStringYYYYMMDDWithTime: infoMedicionClimaticaCabecera[@"fechaHora"]];
                            }
                            if ([infoMedicionClimaticaCabecera objectForKey:@"proveedorInformacion"] != [NSNull null]) {
                                medicionInformacionClimaticaCabecera.nombreProveedor = [infoMedicionClimaticaCabecera objectForKey:@"proveedorInformacion"];
                            }
                            
                            if ([infoMedicionClimaticaCabecera objectForKey:@"mediciones_detalles"] != [NSNull null]) {
                                NSDictionary *listaInfoDetallesMedicionClimatica = [infoMedicionClimaticaCabecera objectForKey:@"mediciones_detalles"];
                                
                                NSMutableArray *listaInstanciasDetalleMedicionClimatica = [NSMutableArray new];
                                
                                for (NSDictionary *infoDetalleMedicionClimatica in listaInfoDetallesMedicionClimatica) {
                                    
                                    SFMedicionInformacionClimaticaDetalle *medicionInformacionClimaticaDetalle = [SFMedicionInformacionClimaticaDetalle new];
                                    
                                    if ([infoDetalleMedicionClimatica objectForKey:@"nroRenglon"] != [NSNull null]) {
                                        medicionInformacionClimaticaDetalle.nroRenglon = [[infoDetalleMedicionClimatica objectForKey:@"nroRenglon"] integerValue];
                                    }
                                    if ([infoDetalleMedicionClimatica objectForKey:@"valor"] != [NSNull null]) {
                                        medicionInformacionClimaticaDetalle.valorMedicion = [[infoDetalleMedicionClimatica objectForKey:@"valor"] floatValue];
                                    }
                                    
                                    if ([infoDetalleMedicionClimatica objectForKey:@"tipoMedicionClimatica"] != [NSNull null]) {
                                        medicionInformacionClimaticaDetalle.nombreTipoMedicion = [infoDetalleMedicionClimatica objectForKey:@"tipoMedicionClimatica"];
                                    }
                                    [listaInstanciasDetalleMedicionClimatica addObject:medicionInformacionClimaticaDetalle];
                                }
                                
                                medicionInformacionClimaticaCabecera.listaDetallesMedicionInformacionClimatica = [NSArray arrayWithArray:listaInstanciasDetalleMedicionClimatica];
                            }
                            
                            [listaMedicionesClimaticas addObject:medicionInformacionClimaticaCabecera];
                        }
                        nuevaInstancia.medicionesClimaticasAntes = [NSArray arrayWithArray:listaMedicionesClimaticas];
                    }
                    
                    [listaInstancias addObject:nuevaInstancia];
                }
                
                respuesta.listaDatosCruzados = [NSArray arrayWithArray:listaInstancias];
                
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
