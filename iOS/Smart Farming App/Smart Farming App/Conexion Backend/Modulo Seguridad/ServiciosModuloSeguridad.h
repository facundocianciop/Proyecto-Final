//
//  ModuloSeguridad.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 9/21/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "BaseServicios.h"

#import "SolicitudInicioSesion.h"
#import "RespuestaInicioSesion.h"

#import "RespuestaMostrarUsuario.h"

@interface ServiciosModuloSeguridad : BaseServicios

#pragma mark - Public

+(void) iniciarSesion:(SolicitudInicioSesion*)SolicitudInicioSesion
      completionBlock:(SuccessBlock)completionBlock
         failureBlock:(FailureBlock)failureBlock;

+(void) finalizarSesion:(SuccessBlock)completionBlock
           failureBlock:(FailureBlock)failureBlock;

+(void) mostrarUsuario:(SuccessBlock)completionBlock
          failureBlock:(FailureBlock)failureBlock;

@end
