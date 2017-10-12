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

@interface ServiciosModuloSeguridad : BaseServicios

#pragma mark - Public

+(void) iniciarSesion:(SolicitudInicioSesion*)SolicitudInicioSesion
      completionBlock:(SuccessBlock)completionBlock
         failureBlock:(FailureBlock)failureBlock;



+(void)authenticate:(NSString *)username
           password:(NSString *)password
    completionBlock:(HTTPOperationCompletionBlock)completionBlock
       failureBlock:(HTTPOperationFailureBlock)failureBlock;

+(void)signOut:(HTTPOperationCompletionBlock)completionBlock
  failureBlock:(HTTPOperationFailureBlock)failureBlock;

+(void)     signUp:(NSString *)razonSocial
              cuit:(NSString*)cuit
          contacto:(NSString *)contacto
             email:(NSString *)email
          telefono:(NSString *)telefono
   completionBlock:(HTTPOperationCompletionBlock)completionBlock
      failureBlock:(HTTPOperationFailureBlock)failureBlock;


+(void)forgotUserCredentials:(NSString *)razonSocial
                        cuit:(NSString *)cuit
                       email:(NSString *)email
             completionBlock:(HTTPOperationCompletionBlock)completionBlock
                failureBlock:(HTTPOperationFailureBlock)failureBlock;

@end
