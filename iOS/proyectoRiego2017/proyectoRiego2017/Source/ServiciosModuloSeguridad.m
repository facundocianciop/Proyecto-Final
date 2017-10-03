//
//  ModuloSeguridad.m
//  proyectoRIego2017
//
//  Created by Facundo José Palma on 9/21/17.
//  Copyright © 2017 Facundo José Palma. All rights reserved.
//

#import "ServiciosModuloSeguridad.h"
#import "ContextoUsuario.h"

// LOGIN

#define OPERATION_LOGIN             @"login"

// LOGOUT

#define OPERATION_LOGOUT            @"cerrar_sesion"

// SIGNUP

#define OPERATION_SIGNUP            @"email_registrarme"

// FORGOT CREDENTIALS

#define OPERATION_FORGOT            @"email_olvide_mis_datos"

@interface ServiciosModuloSeguridad()

@property (nonatomic, strong) NSString *sessionId;

@end

@implementation ServiciosModuloSeguridad

#pragma mark - Public

/**
 * login
 * http://190.15.203.5/comercial_android/login.php?login_usuario=testUser&login_password=99129934
 */
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

/**
 * cerrar_sesion
 *
 * http://190.15.203.5/comercial_android/cerrar_sesion.php?nro_usuario=7&nro_sesion=e7514ee8e8aea5dba2d495ad98f8847
 */
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

/**
 * email_registrarme
 *
 * http://190.15.203.5/comercial_android/email_registrarme.php?razon_social=Prueba&cuit=11223344556&persona_contacto=JuanPerez&email=pruebas.app@bolsamza.com.ar&telefono=444-5555
 
 */

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

/**
 * email_olvide_mis_datos
 *
 * http://190.15.203.5/comercial_android/email_olvide_mis_datos.php?razon_social=Prueba&cuit=11223344556&email=pruebas.app@bolsamza.com.ar
 */
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
