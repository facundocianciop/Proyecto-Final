//
//  ModuloSeguridad.m
//  Smart Farming App
//
//  Created by Facundo José Palma on 9/21/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "ServiciosModuloSeguridad.h"
#import "ContextoUsuario.h"

#import "SFUtils.h"

#pragma mark - Operaciones

#define OPERATION_REGISTRARSE                           @"registrarse"
#define OPERATION_INICIAR_SESION                        @"iniciarSesion"
#define OPERATION_FINALIZAR_SESION                      @"finalizarSesion"
#define OPERATION_MOSTRAR_USUARIO                       @"mostrarUsuario"
#define OPERATION_MODIFICAR_USUARIO                     @"modificarUsuario"
#define OPERATION_CAMBIAR_CONTRASENIA                   @"cambiarContrasenia"

#define OPERATION_RECUPERAR_CUENTA                      @"recuperarCuenta"
#define OPERATION_CAMBIAR_CONTRASENIA_RECUPERAR_CUENTA  @"cambiarContraseniaRecuperarCuenta"
#define OPERATION_ELIMINAR_USUARIO                      @"eliminarUsuario"


@interface ServiciosModuloSeguridad()

@property (nonatomic, strong) NSString *sessionId;

@end

@implementation ServiciosModuloSeguridad

#pragma mark - Public

+(void) registrarUsuario:(SolicitudRegistrarUsuario*)solicitudRegistrarUsuario
         completionBlock:(SuccessBlock)completionBlock
            failureBlock:(FailureBlock)failureBlock {
    
    NSMutableDictionary *parametrosLlamada = [NSMutableDictionary new];
    if (solicitudRegistrarUsuario.usuario) {
        [parametrosLlamada setObject:solicitudRegistrarUsuario.usuario forKey:KEY_USUARIO];
    }
    if (solicitudRegistrarUsuario.email) {
        [parametrosLlamada setObject:solicitudRegistrarUsuario.email forKey:KEY_EMAIL];
    }
    if (solicitudRegistrarUsuario.contrasenia) {
        [parametrosLlamada setObject:solicitudRegistrarUsuario.contrasenia forKey:KEY_CONTRASENIA];
    }
    if (solicitudRegistrarUsuario.nombre) {
        [parametrosLlamada setObject:solicitudRegistrarUsuario.nombre forKey:KEY_NOMBRE_USUARIO];
    }
    if (solicitudRegistrarUsuario.apellido) {
        [parametrosLlamada setObject:solicitudRegistrarUsuario.apellido forKey:KEY_APELLIDO_USUARIO];
    }
    if (solicitudRegistrarUsuario.fechaNacimiento) {
        [parametrosLlamada setObject:[SFUtils formatDateYYYYMMDD: solicitudRegistrarUsuario.fechaNacimiento] forKey:KEY_FECHA_NACIMIENTO];
    }
    if (solicitudRegistrarUsuario.dni) {
        [parametrosLlamada setObject:[NSString stringWithFormat:@"%li", solicitudRegistrarUsuario.dni] forKey:KEY_DNI];
    }
    if (solicitudRegistrarUsuario.cuit) {
        [parametrosLlamada setObject:solicitudRegistrarUsuario.cuit forKey:KEY_CUIT];
    }
    if (solicitudRegistrarUsuario.domicilio) {
        [parametrosLlamada setObject:solicitudRegistrarUsuario.domicilio forKey:KEY_DOMICILIO];
    }
    
    [[HTTPConector instance] httpOperation:OPERATION_REGISTRARSE method:METHOD_PUT withParameters:parametrosLlamada completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaServicioBase *respuesta = [RespuestaServicioBase new];
        
        [ServiciosModuloSeguridad armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        completionBlock(respuesta);
        
    } failureBlock:^(NSError *error) {
        failureBlock([ServiciosModuloSeguridad armarErrorServicio:error]);
    }];
}

+(void) iniciarSesion:(SolicitudInicioSesion*)SolicitudInicioSesion
      completionBlock:(SuccessBlock)completionBlock
         failureBlock:(FailureBlock)failureBlock {
    
    NSMutableDictionary *parametrosLlamada = [NSMutableDictionary new];
    if (SolicitudInicioSesion.usuario) {
         [parametrosLlamada setObject:SolicitudInicioSesion.usuario forKey:KEY_USUARIO];
    }
    if (SolicitudInicioSesion.contrasenia) {
        [parametrosLlamada setObject:SolicitudInicioSesion.contrasenia forKey:KEY_CONTRASENIA];
    }
    [parametrosLlamada setObject:@0 forKey:KEY_TIPO_SESION];
    
    [[HTTPConector instance] httpOperation:OPERATION_INICIAR_SESION method:METHOD_POST withParameters:parametrosLlamada completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaInicioSesion *respuesta = [RespuestaInicioSesion new];
        
        NSDictionary *datosOperacion = [ServiciosModuloSeguridad armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        if (respuesta.resultado && datosOperacion) {
            
            [ContextoUsuario instanceWithUsername:[datosOperacion objectForKey:KEY_USUARIO]];
            
            respuesta.username = [datosOperacion objectForKey:KEY_USUARIO];
            respuesta.nombre = [datosOperacion objectForKey:KEY_NOMBRE_USUARIO];
            respuesta.apellido = [datosOperacion objectForKey:KEY_APELLIDO_USUARIO];
        }
        
        completionBlock(respuesta);
        
    } failureBlock:^(NSError *error) {
        failureBlock([ServiciosModuloSeguridad armarErrorServicio:error]);
    }];
}

+(void) finalizarSesion:(SuccessBlock)completionBlock
          failureBlock:(FailureBlock)failureBlock {
    
    [[HTTPConector instance] httpOperation:OPERATION_FINALIZAR_SESION method:METHOD_POST withParameters:nil completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaInicioSesion *respuesta = [RespuestaInicioSesion new];
        
        [ServiciosModuloSeguridad armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        completionBlock(respuesta);
        
    } failureBlock:^(NSError *error) {
        failureBlock([ServiciosModuloSeguridad armarErrorServicio:error]);
    }];
}
    
+(void) mostrarUsuario:(SuccessBlock)completionBlock
       failureBlock:(FailureBlock)failureBlock {
    
    [[HTTPConector instance] httpOperation:OPERATION_MOSTRAR_USUARIO method:METHOD_GET withParameters:nil completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaMostrarUsuario *respuesta = [RespuestaMostrarUsuario new];
        
        NSDictionary *datosOperacion = [ServiciosModuloSeguridad armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        if (respuesta.resultado && datosOperacion) {
            @try {
                respuesta.username = [datosOperacion objectForKey:KEY_USUARIO];
                respuesta.email = [datosOperacion objectForKey:KEY_EMAIL];
                
                respuesta.nombre = [datosOperacion objectForKey:KEY_NOMBRE_USUARIO];
                respuesta.apellido = [datosOperacion objectForKey:KEY_APELLIDO_USUARIO];
                
                if ([datosOperacion objectForKey:KEY_FECHA_NACIMIENTO]!= [NSNull null]) {
                    respuesta.fechaNacimiento = [SFUtils dateFromStringYYYYMMDD:datosOperacion[KEY_FECHA_NACIMIENTO]];
                }
                if ([datosOperacion objectForKey:KEY_DNI] != [NSNull null]) {
                    respuesta.dni = [[datosOperacion objectForKey:KEY_DNI] integerValue];
                }
                if ([datosOperacion objectForKey:KEY_CUIT] != [NSNull null]) {
                    respuesta.cuit = [datosOperacion objectForKey:KEY_CUIT];;
                }
                if ([datosOperacion objectForKey:KEY_DOMICILIO] != [NSNull null]) {
                    respuesta.domicilio = [datosOperacion objectForKey:KEY_DOMICILIO];
                }
                completionBlock(respuesta);
            } @catch (NSException *exception) {
                completionBlock(respuesta);
            }
        } else {
            completionBlock(respuesta);
        }
    } failureBlock:^(NSError *error) {
        failureBlock([BaseServicios armarErrorServicio:error]);
    }];
}

+(void) modificarUsuario:(SolicitudModificarUsuario*)solicitudModificarUsuario
         completionBlock:(SuccessBlock)completionBlock
            failureBlock:(FailureBlock)failureBlock {
    
    NSMutableDictionary *parametrosLlamada = [NSMutableDictionary new];
    if (solicitudModificarUsuario.email) {
        [parametrosLlamada setObject:solicitudModificarUsuario.email forKey:KEY_EMAIL];
    }
    if (solicitudModificarUsuario.nombre) {
        [parametrosLlamada setObject:solicitudModificarUsuario.nombre forKey:KEY_NOMBRE_USUARIO];
    }
    if (solicitudModificarUsuario.apellido) {
        [parametrosLlamada setObject:solicitudModificarUsuario.apellido forKey:KEY_APELLIDO_USUARIO];
    }
    if (solicitudModificarUsuario.fechaNacimiento) {
        [parametrosLlamada setObject:[SFUtils formatDateYYYYMMDD: solicitudModificarUsuario.fechaNacimiento] forKey:KEY_FECHA_NACIMIENTO];
    }
    if (solicitudModificarUsuario.dni) {
        [parametrosLlamada setObject:[NSString stringWithFormat:@"%li", solicitudModificarUsuario.dni] forKey:KEY_DNI];
    }
    if (solicitudModificarUsuario.cuit) {
        [parametrosLlamada setObject:solicitudModificarUsuario.cuit forKey:KEY_CUIT];
    }
    if (solicitudModificarUsuario.domicilio) {
        [parametrosLlamada setObject:solicitudModificarUsuario.domicilio forKey:KEY_DOMICILIO];
    }
    
    [[HTTPConector instance] httpOperation:OPERATION_MODIFICAR_USUARIO method:METHOD_POST withParameters:parametrosLlamada completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaServicioBase *respuesta = [RespuestaServicioBase new];
        
        [ServiciosModuloSeguridad armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        completionBlock(respuesta);
        
    } failureBlock:^(NSError *error) {
        failureBlock([ServiciosModuloSeguridad armarErrorServicio:error]);
    }];
}

+(void) cambiarContrasenia:(SolicitudCambiarContrasenia*)solicitudCambiarContrasenia
         completionBlock:(SuccessBlock)completionBlock
            failureBlock:(FailureBlock)failureBlock {
    
    NSMutableDictionary *parametrosLlamada = [NSMutableDictionary new];
    if (solicitudCambiarContrasenia.contraseniaActual) {
        [parametrosLlamada setObject:solicitudCambiarContrasenia.contraseniaActual forKey:KEY_CONTRASENIA_VIEJA];
    }
    if (solicitudCambiarContrasenia.contraseniaNueva) {
        [parametrosLlamada setObject:solicitudCambiarContrasenia.contraseniaNueva forKey:KEY_CONTRASENIA_NUEVA];
    }
    
    [[HTTPConector instance] httpOperation:OPERATION_CAMBIAR_CONTRASENIA method:METHOD_POST withParameters:parametrosLlamada completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaServicioBase *respuesta = [RespuestaServicioBase new];
        
        [ServiciosModuloSeguridad armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        completionBlock(respuesta);
        
    } failureBlock:^(NSError *error) {
        failureBlock([ServiciosModuloSeguridad armarErrorServicio:error]);
    }];
}

+(void) recuperarCuenta:(SolicitudRecuperarCuenta*)solicitudRecuperarCuenta
         completionBlock:(SuccessBlock)completionBlock
            failureBlock:(FailureBlock)failureBlock {
    
    NSMutableDictionary *parametrosLlamada = [NSMutableDictionary new];
    if (solicitudRecuperarCuenta.email) {
        [parametrosLlamada setObject:solicitudRecuperarCuenta.email forKey:KEY_EMAIL];
    }
    
    [[HTTPConector instance] httpOperation:OPERATION_RECUPERAR_CUENTA method:METHOD_POST withParameters:parametrosLlamada completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaRecuperarCuenta *respuesta = [RespuestaRecuperarCuenta new];
        
        NSDictionary *datosOperacion = [ServiciosModuloSeguridad armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        if (respuesta.resultado && datosOperacion) {
            @try {
                if ([datosOperacion objectForKey:KEY_KEY_USUARIO]) {
                    respuesta.username = [datosOperacion objectForKey:KEY_KEY_USUARIO];
                }
                
                completionBlock(respuesta);
            } @catch (NSException *exception) {
                completionBlock(respuesta);
            }
        } else {
            completionBlock(respuesta);
        }
    } failureBlock:^(NSError *error) {
        failureBlock([ServiciosModuloSeguridad armarErrorServicio:error]);
    }];
}

+(void) cambiarContraseniaRecuperarCuenta:(SolicitudRecuperarCuentaCambiarContrasenia*)solicitudRecuperarCuentaCambiarContrasenia
        completionBlock:(SuccessBlock)completionBlock
           failureBlock:(FailureBlock)failureBlock {
    
    NSMutableDictionary *parametrosLlamada = [NSMutableDictionary new];
    if (solicitudRecuperarCuentaCambiarContrasenia.username) {
        [parametrosLlamada setObject:solicitudRecuperarCuentaCambiarContrasenia.username forKey:KEY_USUARIO];
    }
    if (solicitudRecuperarCuentaCambiarContrasenia.codigoVerificacion) {
        [parametrosLlamada setObject:solicitudRecuperarCuentaCambiarContrasenia.codigoVerificacion forKey:KEY_CODIGO_VERIFICACION];
    }
    if (solicitudRecuperarCuentaCambiarContrasenia.contraseniaNueva) {
        [parametrosLlamada setObject:solicitudRecuperarCuentaCambiarContrasenia.contraseniaNueva forKey:KEY_CONTRASENIA_NUEVA];
    }
    
    [[HTTPConector instance] httpOperation:OPERATION_CAMBIAR_CONTRASENIA_RECUPERAR_CUENTA method:METHOD_POST withParameters:parametrosLlamada completionBlock:^(NSDictionary *responseObject) {
        
        RespuestaServicioBase *respuesta = [RespuestaServicioBase new];
        
        [ServiciosModuloSeguridad armarRespuestaServicio:respuesta withResponseObject:responseObject];
        
        completionBlock(respuesta);
        
    } failureBlock:^(NSError *error) {
        failureBlock([ServiciosModuloSeguridad armarErrorServicio:error]);
    }];
}

@end
