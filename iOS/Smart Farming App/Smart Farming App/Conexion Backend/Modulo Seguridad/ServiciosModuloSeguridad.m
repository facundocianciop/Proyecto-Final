//
//  ModuloSeguridad.m
//  Smart Farming App
//
//  Created by Facundo José Palma on 9/21/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "ServiciosModuloSeguridad.h"
#import "ContextoUsuario.h"

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



+(void)authenticate:(NSString *)username
           password:(NSString *)password
    completionBlock:(HTTPOperationCompletionBlock)completionBlock
       failureBlock:(HTTPOperationFailureBlock)failureBlock {
    
    NSMutableDictionary *loginParams = [NSMutableDictionary new];
    [loginParams setObject:username forKey:PARAM_USERNAME];
    [loginParams setObject:password forKey:PARAM_PASSWORD];
    
    [[HTTPConector instance] httpOperation:OPERATION_LOGIN method:METHOD_POST withParameters:loginParams completionBlock:^(NSArray *responseObject) {
        
        if (responseObject.count){
            
            NSDictionary *responseDict = [responseObject firstObject];
            NSString *sessionId = [responseDict objectForKey:PARAM_SESSION_ID];
            NSNumber *userId = [responseDict objectForKey:PARAM_USER_ID];
            NSNumber *clientId = [responseDict objectForKey:PARAM_CLIENT_ID];
            NSString *clientDescription = [responseDict objectForKey:PARAM_RAZON_SOCIAL];
            
            if (sessionId && [userId integerValue] && [clientId integerValue])
            {
                [ContextoUsuario instanceWithSessionId:sessionId userId:[userId longValue] clientId:[clientId longValue] clientDescription:clientDescription];
                completionBlock(responseObject);
            }
            else
            {
                failureBlock(nil);
            }
        }
        
    } failureBlock:^(NSError *error) {
        failureBlock(error);
    }];
}

+(void)signOut:(HTTPOperationCompletionBlock)completionBlock
  failureBlock:(HTTPOperationFailureBlock)failureBlock {
    
    NSString *sessionID = [[ContextoUsuario instance] currentSessionId];
    long userId = [[ContextoUsuario instance] currentUserId];
    
    NSMutableDictionary *signOutParams = [NSMutableDictionary new];
    [signOutParams setObject:[NSNumber numberWithLong:userId] forKey:PARAM_USER_ID];
    [signOutParams setObject:sessionID forKey:PARAM_SESSION_ID];
    
    [[HTTPConector instance] httpOperation:OPERATION_LOGOUT method:METHOD_POST withParameters:signOutParams completionBlock:^(NSArray *responseObject) {
        
        // Delete User sensitive data
        [[ContextoUsuario instance] invalidateContext];
        
        completionBlock(responseObject);
    } failureBlock:^(NSError *error) {
        failureBlock(error);
    }];
}


+(void)     signUp:(NSString *)razonSocial
              cuit:(NSString *)cuit
          contacto:(NSString *)contacto
             email:(NSString *)email
          telefono:(NSString *)telefono
   completionBlock:(HTTPOperationCompletionBlock)completionBlock
      failureBlock:(HTTPOperationFailureBlock)failureBlock {
    
    NSMutableDictionary *signUpParams = [NSMutableDictionary new];
    [signUpParams setObject:razonSocial forKey:PARAM_RAZON_SOCIAL];
    [signUpParams setObject:cuit forKey:PARAM_CUIT];
    [signUpParams setObject:contacto forKey:PARAM_CONTACT_INFO];
    [signUpParams setObject:email forKey:PARAM_EMAIL];
    [signUpParams setObject:telefono forKey:PARAM_PHONE];
    
    [[HTTPConector instance] httpOperation:OPERATION_SIGNUP method:METHOD_POST withParameters:signUpParams completionBlock:^(NSArray *responseObject) {
        completionBlock(responseObject);
    } failureBlock:^(NSError *error) {
        failureBlock(error);
    }];
}


+(void)forgotUserCredentials:(NSString *)razonSocial
                        cuit:(NSString *)cuit
                       email:(NSString *)email
             completionBlock:(HTTPOperationCompletionBlock)completionBlock
                failureBlock:(HTTPOperationFailureBlock)failureBlock {
    
    NSMutableDictionary *forgotParams = [NSMutableDictionary new];
    [forgotParams setObject:razonSocial forKey:PARAM_RAZON_SOCIAL];
    [forgotParams setObject:cuit forKey:PARAM_CUIT];
    [forgotParams setObject:email forKey:PARAM_EMAIL];
    
    [[HTTPConector instance] httpOperation:OPERATION_FORGOT method:METHOD_POST withParameters:forgotParams completionBlock:^(NSArray *responseObject) {
        completionBlock(responseObject);
    } failureBlock:^(NSError *error) {
        failureBlock(error);
    }];
}

@end
