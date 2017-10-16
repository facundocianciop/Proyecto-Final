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

@interface ServiciosModuloFinca : BaseServicios

+(void) mostrarFincasEncargadoWithCompletionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock;

+(void) obtenerFincasEstadoPendiente:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock;

+(void) obtenerFincasPorUsuario:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock;

+(void) buscarRoles:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock;

@end
