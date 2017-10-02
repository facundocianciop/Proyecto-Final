//
//  ServiciosModuloFinca.h
//  proyectoRIego2017
//
//  Created by Facundo José Palma on 9/21/17.
//  Copyright © 2017 Facundo José Palma. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "BaseServicios.h"

@interface ServiciosModuloFinca : NSObject

+(void)clientPaymentTypes:(HTTPOperationCompletionBlock)completionBlock
             failureBlock:(HTTPOperationFailureBlock)failureBlock;

@end
