//
//  ServiciosModuloFinca.m
//  Smart Farming App
//
//  Created by Facundo José Palma on 9/21/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "ServiciosModuloFinca.h"
#import "ContextoUsuario.h"

#pragma mark - operaciones

#define OPERATION_MOSTRAR_FINCAS_ENCARGADO          @"mostrarFincasEncargado"

#define OPERATION_BUSCAR_ROLES                      @"buscarRoles"
#define OPERATION_OBTENER_FINCAS_POR_USUARIO        @"obtenerFincasPorUsuario"

#define OPERATION_OBTENER_FINCAS_ESTADO_PENDIENTE   @"obtenerFincasEstadoPendiente"

#define OPERATION_BUSCAR_FINCA_ID                   @"buscarFincaId"
#define OPERATION_DEVOLVER_PERMISOS                 @"devolverPermisos"

#define OPERATION_OBTENER_PROVEEDOR_FINCA           @"obtenerProveedorFinca"

@implementation ServiciosModuloFinca

+(void) mostrarFincasEncargadoWithCompletionBlock:(SuccessBlock)completionBlock
                                     failureBlock:(FailureBlock)failureBlock {
    
    [[HTTPConector instance] httpOperation:OPERATION_MOSTRAR_FINCAS_ENCARGADO method:METHOD_GET withParameters:nil completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaMostrarFincas *respuesta = [RespuestaMostrarFincas new];
        
        NSDictionary *datosOperacion = [ServiciosModuloFinca armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        if (respuesta.resultado && datosOperacion) {
            
            NSMutableArray *fincas = [NSMutableArray new];
            
            for (NSDictionary *datos in datosOperacion) {
                
                SFFinca *finca = [SFFinca new];
                
                if ([datos objectForKey:KEY_ID_FINCA] != [NSNull null]) {
                    finca.idFinca = [[datos objectForKey:KEY_ID_FINCA] longLongValue];
                }
                if ([datos objectForKey:KEY_NOMBRE_FINCA_RESPUESTA] != [NSNull null]) {
                    finca.nombre = [datos objectForKey:KEY_NOMBRE_FINCA_RESPUESTA];
                }
                
                if ([datos objectForKey:KEY_TAMANIO] != [NSNull null]) {
                    finca.tamanio = [[datos objectForKey:KEY_TAMANIO] integerValue];
                }
                if ([datos objectForKey:KEY_UBICACION] != [NSNull null]) {
                    finca.ubicacion = [datos objectForKey:KEY_UBICACION];
                }
                if ([datos objectForKey:KEY_DIRECCION_LEGAL] != [NSNull null]) {
                    finca.direccionLegal = [datos objectForKey:KEY_DIRECCION_LEGAL];
                }
                
                [fincas addObject:finca];
            }
            respuesta.fincas = fincas;
        }
        
        completionBlock(respuesta);
        
    } failureBlock:^(NSError *error) {
        failureBlock([BaseServicios armarErrorServicio:error]);
    }];
}

+(void) buscarRoles:(SuccessBlock)completionBlock
       failureBlock:(FailureBlock)failureBlock {
    
    [[HTTPConector instance] httpOperation:OPERATION_BUSCAR_ROLES method:METHOD_GET withParameters:nil completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaBuscarRoles *respuesta = [RespuestaBuscarRoles new];
        
        NSDictionary *datosOperacion = [ServiciosModuloFinca armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        if (respuesta.resultado && datosOperacion) {
            
            NSMutableArray *roles = [NSMutableArray new];
            
            for (NSDictionary *datos in datosOperacion) {
                
                if ([datos objectForKey:KEY_NOMBRE_ROL] != [NSNull null]) {
                    NSString *rol = [datos objectForKey:KEY_NOMBRE_ROL];
                    if ([rol isKindOfClass:[NSString class]] && ![rol isEqualToString:@""]) {
                        [roles addObject:rol];
                    }
                }
            }
            respuesta.nombreRoles = roles;
        }
        completionBlock(respuesta);
    } failureBlock:^(NSError *error) {
        failureBlock([BaseServicios armarErrorServicio:error]);
    }];
}

+(void) obtenerFincasPorUsuario:(SuccessBlock)completionBlock
                        failureBlock:(FailureBlock)failureBlock {
    
    [[HTTPConector instance] httpOperation:OPERATION_OBTENER_FINCAS_POR_USUARIO method:METHOD_GET withParameters:nil completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaMostrarFincas *respuesta = [RespuestaMostrarFincas new];
        
        NSDictionary *datosOperacion = [ServiciosModuloFinca armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        if (respuesta.resultado && datosOperacion) {
            
            NSMutableArray *fincas = [NSMutableArray new];
            
            for (NSDictionary *datos in datosOperacion) {
                
                SFFinca *finca = [SFFinca new];
                
                if ([datos objectForKey:KEY_ID_FINCA] != [NSNull null]) {
                    finca.idFinca = [[datos objectForKey:KEY_ID_FINCA] longLongValue];
                }
                if ([datos objectForKey:KEY_NOMBRE_FINCA_RESPUESTA] != [NSNull null]) {
                    finca.nombre = [datos objectForKey:KEY_NOMBRE_FINCA_RESPUESTA];
                }
                
                if ([datos objectForKey:KEY_TAMANIO] != [NSNull null]) {
                    finca.tamanio = [[datos objectForKey:KEY_TAMANIO] integerValue];
                }
                if ([datos objectForKey:KEY_UBICACION] != [NSNull null]) {
                    finca.ubicacion = [datos objectForKey:KEY_UBICACION];
                }
                if ([datos objectForKey:KEY_DIRECCION_LEGAL] != [NSNull null]) {
                    finca.direccionLegal = [datos objectForKey:KEY_DIRECCION_LEGAL];
                }
                if ([datos objectForKey:KEY_NOMBRE_ROL] != [NSNull null]) {
                    finca.rolUsuario = [datos objectForKey:KEY_NOMBRE_ROL];
                }
                
                [fincas addObject:finca];
            }
            respuesta.fincas = fincas;
        }
        completionBlock(respuesta);
    } failureBlock:^(NSError *error) {
        failureBlock([BaseServicios armarErrorServicio:error]);
    }];
}

+(void) obtenerFincasEstadoPendiente:(SuccessBlock)completionBlock
                        failureBlock:(FailureBlock)failureBlock {
    
    [[HTTPConector instance] httpOperation:OPERATION_OBTENER_FINCAS_ESTADO_PENDIENTE method:METHOD_GET withParameters:nil completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaMostrarFincas *respuesta = [RespuestaMostrarFincas new];
        
        NSDictionary *datosOperacion = [ServiciosModuloFinca armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        if (respuesta.resultado && datosOperacion) {
            
            NSMutableArray *fincas = [NSMutableArray new];
            
            for (NSDictionary *datos in datosOperacion) {
                
                SFFinca *finca = [SFFinca new];
                
                if ([datos objectForKey:KEY_ID_FINCA] != [NSNull null]) {
                    finca.idFinca = [[datos objectForKey:KEY_ID_FINCA] longLongValue];
                }
                if ([datos objectForKey:KEY_NOMBRE_FINCA_RESPUESTA] != [NSNull null]) {
                    finca.nombre = [datos objectForKey:KEY_NOMBRE_FINCA_RESPUESTA];
                }
                
                if ([datos objectForKey:KEY_TAMANIO] != [NSNull null]) {
                    finca.tamanio = [[datos objectForKey:KEY_TAMANIO] integerValue];
                }
                if ([datos objectForKey:KEY_UBICACION] != [NSNull null]) {
                    finca.ubicacion = [datos objectForKey:KEY_UBICACION];
                }
                if ([datos objectForKey:KEY_DIRECCION_LEGAL] != [NSNull null]) {
                    finca.direccionLegal = [datos objectForKey:KEY_DIRECCION_LEGAL];
                }
                
                [fincas addObject:finca];
            }
            respuesta.fincas = fincas;
        }
        completionBlock(respuesta);
    } failureBlock:^(NSError *error) {
        failureBlock([BaseServicios armarErrorServicio:error]);
    }];
}

+(void) buscarFincaId:(SolicitudBuscarFincaId*)solicitudBuscarFincaId completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock {
    
    NSMutableDictionary *parametrosLlamada = [NSMutableDictionary new];
    if (solicitudBuscarFincaId.idFinca) {
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudBuscarFincaId.idFinca] forKey:KEY_ID_FINCA];
    }
    
    [[HTTPConector instance] httpOperation:OPERATION_BUSCAR_FINCA_ID method:METHOD_POST withParameters:parametrosLlamada completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaBuscarFincaId *respuesta = [RespuestaBuscarFincaId new];
        
        NSDictionary *datosOperacion = [ServiciosModuloFinca armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        if (respuesta.resultado && datosOperacion) {
            
            @try {
                SFFinca *finca = [SFFinca new];
                
                if ([datosOperacion objectForKey:KEY_ID_FINCA] != [NSNull null]) {
                    finca.idFinca = [[datosOperacion objectForKey:KEY_ID_FINCA] longLongValue];
                }
                if ([datosOperacion objectForKey:KEY_NOMBRE_FINCA_RESPUESTA] != [NSNull null]) {
                    finca.nombre = [datosOperacion objectForKey:KEY_NOMBRE_FINCA_RESPUESTA];
                }
                
                if ([datosOperacion objectForKey:KEY_TAMANIO] != [NSNull null]) {
                    finca.tamanio = [[datosOperacion objectForKey:KEY_TAMANIO] integerValue];
                }
                if ([datosOperacion objectForKey:KEY_UBICACION] != [NSNull null]) {
                    finca.ubicacion = [datosOperacion objectForKey:KEY_UBICACION];
                }
                if ([datosOperacion objectForKey:KEY_DIRECCION_LEGAL] != [NSNull null]) {
                    finca.direccionLegal = [datosOperacion objectForKey:KEY_DIRECCION_LEGAL];
                }
                
                if ([datosOperacion objectForKey:KEY_NOMBRE_ROL] != [NSNull null]) {
                    finca.rolUsuario = [datosOperacion objectForKey:KEY_NOMBRE_ROL];
                }
                if ([datosOperacion objectForKey:KEY_ID_USUARIO_FINCA] != [NSNull null]) {
                    finca.idUsuarioFinca = [[datosOperacion objectForKey:KEY_ID_USUARIO_FINCA] longLongValue];
                }
                
                respuesta.finca = finca;
                
            } @catch (NSException *exception) {
                completionBlock(respuesta);
            }
        }
        completionBlock(respuesta);
    } failureBlock:^(NSError *error) {
        failureBlock([BaseServicios armarErrorServicio:error]);
    }];
}

+(void) devolverPermisos:(SolicitudDevolverPermisos*)solicitudDevolverPermisos completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock{
    
    NSMutableDictionary *parametrosLlamada = [NSMutableDictionary new];
    if (solicitudDevolverPermisos.idFinca) {
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudDevolverPermisos.idFinca] forKey:KEY_ID_FINCA];
    }
    
    [[HTTPConector instance] httpOperation:OPERATION_DEVOLVER_PERMISOS method:METHOD_POST withParameters:parametrosLlamada completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaDevolverPermisos *respuesta = [RespuestaDevolverPermisos new];
        
        NSDictionary *datosOperacion = [ServiciosModuloFinca armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        if (respuesta.resultado && datosOperacion) {
            
            @try {
                SFConjuntoPermisos *conjuntoPermisos = [SFConjuntoPermisos new];
                
                if ([datosOperacion objectForKey:KEY_PERMISO_PUEDE_ASIGNAR_COMPONENTE_SENSOR] != [NSNull null]) {
                    conjuntoPermisos.puedeAsignarComponenteSensor = [[datosOperacion objectForKey:KEY_PERMISO_PUEDE_ASIGNAR_COMPONENTE_SENSOR] boolValue];
                }
                if ([datosOperacion objectForKey:KEY_PERMISO_PUEDE_ASIGNAR_CULTIVO] != [NSNull null]) {
                    conjuntoPermisos.puedeAsignarCultivo = [[datosOperacion objectForKey:KEY_PERMISO_PUEDE_ASIGNAR_CULTIVO] boolValue];
                }
                if ([datosOperacion objectForKey:KEY_PERMISO_PUEDE_ASIGNAR_MECRIEGO_A_FINCA] != [NSNull null]) {
                    conjuntoPermisos.puedeAsignarMecRiegoAFinca = [[datosOperacion objectForKey:KEY_PERMISO_PUEDE_ASIGNAR_MECRIEGO_A_FINCA] boolValue];
                }
                if ([datosOperacion objectForKey:KEY_PERMISO_PUEDE_ASIGNAR_MECRIEGO_A_SECTOR] != [NSNull null]) {
                    conjuntoPermisos.puedeAsignarMecRiegoASector = [[datosOperacion objectForKey:KEY_PERMISO_PUEDE_ASIGNAR_MECRIEGO_A_SECTOR] boolValue];
                }
                if ([datosOperacion objectForKey:KEY_PERMISO_PUEDE_CONFIGURAR_OBTENCION_INFO_EXTERNA] != [NSNull null]) {
                   conjuntoPermisos.puedeConfigurarObtencionInfoExterna  = [[datosOperacion objectForKey:KEY_PERMISO_PUEDE_CONFIGURAR_OBTENCION_INFO_EXTERNA] boolValue];
                }
                if ([datosOperacion objectForKey:KEY_PERMISO_PUEDE_CREAR_COMPONENTE_SENSOR] != [NSNull null]) {
                   conjuntoPermisos.puedeCrearComponenteSensor = [[datosOperacion objectForKey:KEY_PERMISO_PUEDE_CREAR_COMPONENTE_SENSOR] boolValue];
                }
                if ([datosOperacion objectForKey:KEY_PERMISO_PUEDE_CREAR_CONFIGURACION_RIEGO] != [NSNull null]) {
                   conjuntoPermisos.puedeCrearConfiguracionRiego = [[datosOperacion objectForKey:KEY_PERMISO_PUEDE_CREAR_CONFIGURACION_RIEGO] boolValue];
                }
                if ([datosOperacion objectForKey:KEY_PERMISO_PUEDE_CREAR_SECTOR] != [NSNull null]) {
                   conjuntoPermisos.puedeCrearSector = [[datosOperacion objectForKey:KEY_PERMISO_PUEDE_CREAR_SECTOR] boolValue];
                }
                if ([datosOperacion objectForKey:KEY_PERMISO_PUEDE_GENERAR_INFORME_CRUZADO_RIEGO_MEDICION] != [NSNull null]) {
                   conjuntoPermisos.puedeGenerarInformeCruzadoRiegoMedicion = [[datosOperacion objectForKey:KEY_PERMISO_PUEDE_GENERAR_INFORME_CRUZADO_RIEGO_MEDICION] boolValue];
                }
                if ([datosOperacion objectForKey:KEY_PERMISO_PUEDE_GENERAR_INFORME_ESTADO_ACTUAL_SECTORES] != [NSNull null]) {
                   conjuntoPermisos.puedeGenerarInformeEstadoActualSectores = [[datosOperacion objectForKey:KEY_PERMISO_PUEDE_GENERAR_INFORME_ESTADO_ACTUAL_SECTORES] boolValue];
                }
                if ([datosOperacion objectForKey:KEY_PERMISO_PUEDE_GENERAR_INFORME_ESTADO_HISTORICO_SECTORES_FINCA] != [NSNull null]) {
                   conjuntoPermisos.puedeGenerarInformeEstadoHistoricoSectoresFinca = [[datosOperacion objectForKey:KEY_PERMISO_PUEDE_GENERAR_INFORME_ESTADO_HISTORICO_SECTORES_FINCA] boolValue];
                }
                if ([datosOperacion objectForKey:KEY_PERMISO_PUEDE_GENERAR_INFORME_EVENTO_PERSONALIZADO] != [NSNull null]) {
                   conjuntoPermisos.puedeGenerarInformeEventoPersonalizado = [[datosOperacion objectForKey:KEY_PERMISO_PUEDE_GENERAR_INFORME_EVENTO_PERSONALIZADO] boolValue];
                }
                if ([datosOperacion objectForKey:KEY_PERMISO_PUEDE_GENERAR_INFORME_HELADAS_HISTORICO] != [NSNull null]) {
                   conjuntoPermisos.puedeGenerarInformeHeladasHistorico = [[datosOperacion objectForKey:KEY_PERMISO_PUEDE_GENERAR_INFORME_HELADAS_HISTORICO] boolValue];
                }
                if ([datosOperacion objectForKey:KEY_PERMISO_PUEDE_GENERAR_INFORME_RIEGO_EN_EJECUCION] != [NSNull null]) {
                   conjuntoPermisos.puedeGenerarInformeRiegoEnEjecucion = [[datosOperacion objectForKey:KEY_PERMISO_PUEDE_GENERAR_INFORME_RIEGO_EN_EJECUCION] boolValue];
                }
                if ([datosOperacion objectForKey:KEY_PERMISO_PUEDE_GENERAR_INFORME_RIEGO_POR_SECTORES_HISTORICO] != [NSNull null]) {
                   conjuntoPermisos.puedeGenerarInformeRiegoPorSectoresHistorico = [[datosOperacion objectForKey:KEY_PERMISO_PUEDE_GENERAR_INFORME_RIEGO_POR_SECTORES_HISTORICO] boolValue];
                }
                if ([datosOperacion objectForKey:KEY_PERMISO_PUEDE_GESTIONAR_COMPONENTE_SENSOR] != [NSNull null]) {
                   conjuntoPermisos.puedeGestionarComponenteSensor = [[datosOperacion objectForKey:KEY_PERMISO_PUEDE_GESTIONAR_COMPONENTE_SENSOR] boolValue];
                }
                if ([datosOperacion objectForKey:KEY_PERMISO_PUEDE_GESTIONAR_CULTIVO_SECTOR] != [NSNull null]) {
                   conjuntoPermisos.puedeGestionarCultivoSector = [[datosOperacion objectForKey:KEY_PERMISO_PUEDE_GESTIONAR_CULTIVO_SECTOR] boolValue];
                }
                if ([datosOperacion objectForKey:KEY_PERMISO_PUEDE_GESTIONAR_EVENTO_PERSONALIZADO] != [NSNull null]) {
                   conjuntoPermisos.puedeGestionarEventoPersonalizado = [[datosOperacion objectForKey:KEY_PERMISO_PUEDE_GESTIONAR_EVENTO_PERSONALIZADO] boolValue];
                }
                if ([datosOperacion objectForKey:KEY_PERMISO_PUEDE_GESTIONAR_FINCA] != [NSNull null]) {
                   conjuntoPermisos.puedeGestionarFinca = [[datosOperacion objectForKey:KEY_PERMISO_PUEDE_GESTIONAR_FINCA] boolValue];
                }
                if ([datosOperacion objectForKey:KEY_PERMISO_PUEDE_GESTIONAR_SECTOR] != [NSNull null]) {
                   conjuntoPermisos.puedeGestionarSector = [[datosOperacion objectForKey:KEY_PERMISO_PUEDE_GESTIONAR_SECTOR] boolValue];
                }
                if ([datosOperacion objectForKey:KEY_PERMISO_PUEDE_GESTIONAR_SENSORES] != [NSNull null]) {
                   conjuntoPermisos.puedeGestionarSensores = [[datosOperacion objectForKey:KEY_PERMISO_PUEDE_GESTIONAR_SENSORES] boolValue];
                }
                if ([datosOperacion objectForKey:KEY_PERMISO_PUEDE_GESTIONAR_USUARIOS_FINCA] != [NSNull null]) {
                   conjuntoPermisos.puedeGestionarUsuariosFinca = [[datosOperacion objectForKey:KEY_PERMISO_PUEDE_GESTIONAR_USUARIOS_FINCA] boolValue];
                }
                if ([datosOperacion objectForKey:KEY_PERMISO_PUEDE_INICIAR_O_DETENER_RIEGO_MANUALMENTE] != [NSNull null]) {
                  conjuntoPermisos.puedeIniciarODetenerRiegoManualmente  = [[datosOperacion objectForKey:KEY_PERMISO_PUEDE_INICIAR_O_DETENER_RIEGO_MANUALMENTE] boolValue];
                }
                if ([datosOperacion objectForKey:KEY_PERMISO_PUEDE_MODIFICAR_CONFIGURACION_RIEGO] != [NSNull null]) {
                  conjuntoPermisos.puedeModificarConfiguracionRiego  = [[datosOperacion objectForKey:KEY_PERMISO_PUEDE_MODIFICAR_CONFIGURACION_RIEGO] boolValue];
                }
                
                respuesta.conjuntoPermisos = conjuntoPermisos;
                
            } @catch (NSException *exception) {
                completionBlock(respuesta);
            }
        }
        completionBlock(respuesta);
    } failureBlock:^(NSError *error) {
        failureBlock([BaseServicios armarErrorServicio:error]);
    }];
}

+(void) obtenerProveedorFinca:(SolicitudObtenerProveedorFinca*)solicitudObtenerProveedorFinca completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock{
    
    NSMutableDictionary *parametrosLlamada = [NSMutableDictionary new];
    if (solicitudObtenerProveedorFinca.idFinca) {
        [parametrosLlamada setObject:[NSNumber numberWithLong:solicitudObtenerProveedorFinca.idFinca] forKey:KEY_ID_FINCA];
    }
    
    [[HTTPConector instance] httpOperation:OPERATION_OBTENER_PROVEEDOR_FINCA method:METHOD_POST withParameters:parametrosLlamada completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaObtenerProveedorFinca *respuesta = [RespuestaObtenerProveedorFinca new];
        
        NSDictionary *datosOperacion = [ServiciosModuloFinca armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        if (respuesta.resultado && datosOperacion) {
            
            @try {
                SFProveedorInformacionClimatica *proveedorInformacionClimatica = [SFProveedorInformacionClimatica new];
                
                if ([datosOperacion objectForKey:KEY_PROVEEDOR_INFO_EXTERNA_NOMBRE_PROVEEDOR] != [NSNull null]) {
                    proveedorInformacionClimatica.nombreProveedor = [datosOperacion objectForKey:KEY_PROVEEDOR_INFO_EXTERNA_NOMBRE_PROVEEDOR];
                }
                
                if ([datosOperacion objectForKey:KEY_PROVEEDOR_INFO_EXTERNA_URL_API] != [NSNull null]) {
                    proveedorInformacionClimatica.urlApi = [datosOperacion objectForKey:KEY_PROVEEDOR_INFO_EXTERNA_URL_API];
                }
                
                if ([datosOperacion objectForKey:KEY_PROVEEDOR_INFO_EXTERNA_FECHA_ALTA_PROVEEDOR_FINCA]!= [NSNull null]) {
                    proveedorInformacionClimatica.fechaAltaProveedorFinca = [SFUtils dateFromStringYYYYMMDD:datosOperacion[KEY_PROVEEDOR_INFO_EXTERNA_FECHA_ALTA_PROVEEDOR_FINCA]];
                }
                if ([datosOperacion objectForKey:KEY_PROVEEDOR_INFO_EXTERNA_FRECUENCIA_MAXIMA_POSIBLE] != [NSNull null]) {
                    proveedorInformacionClimatica.frecuenciaMaximaPosible = [[datosOperacion objectForKey:KEY_PROVEEDOR_INFO_EXTERNA_FRECUENCIA_MAXIMA_POSIBLE] integerValue];
                }
                
                if ([datosOperacion objectForKey:KEY_PROVEEDOR_INFO_EXTERNA_FRECUENCIA_ACTUAL] != [NSNull null]) {
                    proveedorInformacionClimatica.frecuenciaActual = [[datosOperacion objectForKey:KEY_PROVEEDOR_INFO_EXTERNA_FRECUENCIA_ACTUAL] integerValue];
                }
                
                if ([datosOperacion objectForKey:KEY_PROVEEDOR_INFO_EXTERNA_LISTA_TIPO_MEDICION] != [NSNull null]) {
                    NSDictionary *datosListaTipoMedicion = [datosOperacion objectForKey:KEY_PROVEEDOR_INFO_EXTERNA_LISTA_TIPO_MEDICION];
                    
                    NSMutableArray *listaTiposMedicion = [NSMutableArray new];
                    for (NSDictionary *datos in datosListaTipoMedicion) {
                        
                        SFTipoMedicionClimatica *tipoMedicion = [SFTipoMedicionClimatica new];
                        
                        if ([datos objectForKey:KEY_MEDICION_CLIMATICA_ID_TIPO_MEDICION_CLIMATICA] != [NSNull null]) {
                            tipoMedicion.idTipoMedicionClimatica = [[datos objectForKey:KEY_MEDICION_CLIMATICA_ID_TIPO_MEDICION_CLIMATICA] longLongValue];
                        }
                        
                        if ([datos objectForKey:KEY_MEDICION_CLIMATICA_NOMBRE_TIPO_MEDICION_CLIMATICA] != [NSNull null]) {
                            tipoMedicion.nombreTipoMedicionClimatica = [datos objectForKey:KEY_MEDICION_CLIMATICA_NOMBRE_TIPO_MEDICION_CLIMATICA];
                        }
                        if ([datos objectForKey:KEY_MEDICION_CLIMATICA_UNIDAD_MEDICION] != [NSNull null]) {
                            tipoMedicion.unidadMedicion = [datos objectForKey:KEY_MEDICION_CLIMATICA_UNIDAD_MEDICION];
                        }
                        
                        if ([datos objectForKey:KEY_MEDICION_CLIMATICA_FECHA_ALTA_TIPO_MEDICION_CLIMATICA]!= [NSNull null]) {
                            tipoMedicion.fechaAltaTipoMedicionClimatica = [SFUtils dateFromStringYYYYMMDD:datos[KEY_MEDICION_CLIMATICA_FECHA_ALTA_TIPO_MEDICION_CLIMATICA]];
                        }
                        if ([datos objectForKey:KEY_MEDICION_CLIMATICA_FECHA_BAJA_TIPO_MEDICION_CLIMATICA]!= [NSNull null]) {
                            tipoMedicion.fechaBajaTipoMedicionClimatica = [SFUtils dateFromStringYYYYMMDD:datos[KEY_MEDICION_CLIMATICA_FECHA_BAJA_TIPO_MEDICION_CLIMATICA]];
                        }
                        
                        if ([datos objectForKey:KEY_MEDICION_CLIMATICA_HABILITADA] != [NSNull null]) {
                            tipoMedicion.habilitada = [[datos objectForKey:KEY_MEDICION_CLIMATICA_HABILITADA] boolValue];
                        }

                        [listaTiposMedicion addObject:tipoMedicion];
                    }
                    proveedorInformacionClimatica.listaTipoMedicion = listaTiposMedicion;
                }
                respuesta.proveedorInformacionClimatica = proveedorInformacionClimatica;
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
