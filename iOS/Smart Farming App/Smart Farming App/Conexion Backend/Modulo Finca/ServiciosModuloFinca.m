//
//  ServiciosModuloFinca.m
//  Smart Farming App
//
//  Created by Facundo José Palma on 9/21/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "ServiciosModuloFinca.h"
#import "ContextoUsuario.h"

@implementation ServiciosModuloFinca

/**
 * inscripciones_cliente
 * TODO DELETE: http://190.15.203.5/comercial_android/inscripciones_cliente.php?nro_cliente=2112
 */
+(void)clientPaymentTypes:(HTTPOperationCompletionBlock)completionBlock
             failureBlock:(HTTPOperationFailureBlock)failureBlock {
    
    long clientId = [[ContextoUsuario instance] currentClientId];
    
    NSMutableDictionary *params = [NSMutableDictionary new];
    [params setObject:[NSNumber numberWithLong:clientId] forKey:PARAM_CLIENT_ID];
    
    [[HTTPConector instance] httpOperation:@"" method:METHOD_GET withParameters:params completionBlock:^(NSArray *responseObject) {
        completionBlock(responseObject);
    } failureBlock:^(NSError *error) {
        failureBlock(error);
    }];
}

@end
