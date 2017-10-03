//
//  ModuloSeguridad.h
//  proyectoRIego2017
//
//  Created by Facundo José Palma on 9/21/17.
//  Copyright © 2017 Facundo José Palma. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "BaseServicios.h"

@interface ServiciosModuloSeguridad : NSObject

#pragma mark - Public

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
