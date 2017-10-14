//
//  ServiciosModuloFinca.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 9/21/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "BaseServicios.h"

@interface ServiciosModuloFinca : BaseServicios

+(void) mostrarFincasEncargadoWithCompletionBlock:(SuccessBlock)completionBlock
         failureBlock:(FailureBlock)failureBlock;

@end
