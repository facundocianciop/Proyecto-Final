//
//  ModuloSeguridad.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 9/21/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "BaseServicios.h"

#import "SolicitudRegistrarUsuario.h"

#import "SolicitudInicioSesion.h"
#import "RespuestaInicioSesion.h"

#import "RespuestaMostrarUsuario.h"

#import "SolicitudModificarUsuario.h"

#import "SolicitudCambiarContrasenia.h"

#import "SolicitudRecuperarCuenta.h"
#import "RespuestaRecuperarCuenta.h"

#import "SolicitudRecuperarCuentaCambiarContrasenia.h"

@interface ServiciosModuloSeguridad : BaseServicios

#pragma mark - Public

+(void) registrarUsuario:(SolicitudRegistrarUsuario*)SolicitudInicioSesion
         completionBlock:(SuccessBlock)completionBlock
            failureBlock:(FailureBlock)failureBlock;

+(void) iniciarSesion:(SolicitudInicioSesion*)SolicitudInicioSesion
      completionBlock:(SuccessBlock)completionBlock
         failureBlock:(FailureBlock)failureBlock;

+(void) finalizarSesion:(SuccessBlock)completionBlock
           failureBlock:(FailureBlock)failureBlock;

+(void) mostrarUsuario:(SuccessBlock)completionBlock
          failureBlock:(FailureBlock)failureBlock;

+(void) modificarUsuario:(SolicitudModificarUsuario*)solicitudModificarUsuario
         completionBlock:(SuccessBlock)completionBlock
            failureBlock:(FailureBlock)failureBlock;

+(void) cambiarContrasenia:(SolicitudCambiarContrasenia*)solicitudCambiarContrasenia
           completionBlock:(SuccessBlock)completionBlock
              failureBlock:(FailureBlock)failureBlock;

+(void) recuperarCuenta:(SolicitudRecuperarCuenta*)solicitudRecuperarCuenta
        completionBlock:(SuccessBlock)completionBlock
           failureBlock:(FailureBlock)failureBlock;

+(void) cambiarContraseniaRecuperarCuenta:(SolicitudRecuperarCuentaCambiarContrasenia*)solicitudRecuperarCuentaCambiarContrasenia
                          completionBlock:(SuccessBlock)completionBlock
                             failureBlock:(FailureBlock)failureBlock;

@end
