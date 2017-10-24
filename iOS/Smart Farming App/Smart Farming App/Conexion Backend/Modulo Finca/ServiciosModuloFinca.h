//
//  ServiciosModuloFinca.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 9/21/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "BaseServicios.h"

#import "RespuestaMostrarFincas.h"

#import "RespuestaBuscarRoles.h"

#import "SolicitudBuscarFincaId.h"
#import "RespuestaBuscarFincaId.h"

#import "SolicitudDevolverPermisos.h"
#import "RespuestaDevolverPermisos.h"

#import "SolicitudObtenerProveedorFinca.h"
#import "RespuestaObtenerProveedorFinca.h"

@interface ServiciosModuloFinca : BaseServicios

+(void) mostrarFincasEncargadoWithCompletionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock;

+(void) buscarRoles:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock;

+(void) obtenerFincasPorUsuario:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock;

+(void) obtenerFincasEstadoPendiente:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock;

+(void) buscarFincaId:(SolicitudBuscarFincaId*)solicitudBuscarFincaId completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock;

+(void) devolverPermisos:(SolicitudDevolverPermisos*)solicitudDevolverPermisos completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock;

+(void) obtenerProveedorFinca:(SolicitudObtenerProveedorFinca*)solicitudObtenerProveedorFinca completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock;

@end
