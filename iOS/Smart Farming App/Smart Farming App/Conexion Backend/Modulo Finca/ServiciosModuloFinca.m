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

#define OPERATION_BUSCAR_FINCA_ID                    @"buscarFincaId"
#define OPERATION_DEVOLVER_PERMISOS                  @"devolverPermisos"

#define OPERATION_CREAR_FINCA                        @"crearFinca"
#define OPERATION_MODIFICAR_FINCA                    @"modificarFinca"
#define OPERATION_ELIMINAR_FINCA                     @"eliminarFinca"

#define OPERATION_FINCAS_POR_APROBAR                 @"fincasPorAprobar"
#define OPERATION_OBTENER_FINCAS_ESTADO_PENDIENTE    @"obtenerFincasEstadoPendiente"

#define OPERATION_MOSTRAR_FINCAS_ENCARGADO           @"mostrarFincasEncargado"
#define OPERATION_OBTENER_FINCAS_POR_USUARIO         @"obtenerFincasPorUsuario"
#define OPERATION_BUSCAR_USUARIOS_NO_ENCARGADO       @"buscarUsuariosNoEncargado"
#define OPERATION_BUSCAR_USUARIOS_NO_FINCA           @"buscarUsuariosNoFinca"

#define OPERATION_MODIFICAR_ROL_USUARIO              @"modificarRolUsuario"
#define OPERATION_AGREGAR_USUARIO_FINCA              @"agregarUsuarioFinca"
#define OPERATION_ELIMINAR_USUARIO_FINCA             @"eliminarUsuarioFinca"

#define OPERATION_BUSCAR_PROVEEDORES_INFORMACION     @"buscarProveedoresInformacion"

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
                
                finca.idFinca = [[datos objectForKey:KEY_ID_FINCA] longLongValue];
                finca.nombre = [datos objectForKey:KEY_NOMBRE_FINCA_RESPUESTA];
                
                finca.tamanio = [[datos objectForKey:KEY_TAMANIO] integerValue];
                finca.ubicacion = [datos objectForKey:KEY_UBICACION];
                finca.direccionLegal = [datos objectForKey:KEY_DIRECCION_LEGAL];
                
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
                
                finca.idFinca = [[datos objectForKey:KEY_ID_FINCA] longLongValue];
                finca.nombre = [datos objectForKey:KEY_NOMBRE_FINCA_RESPUESTA];
                
                finca.tamanio = [[datos objectForKey:KEY_TAMANIO] integerValue];
                finca.ubicacion = [datos objectForKey:KEY_UBICACION];
                finca.direccionLegal = [datos objectForKey:KEY_DIRECCION_LEGAL];
                
                [fincas addObject:finca];
            }
            respuesta.fincas = fincas;
        }
        
        completionBlock(respuesta);
        
    } failureBlock:^(NSError *error) {
        failureBlock([BaseServicios armarErrorServicio:error]);
    }];
}

@end
