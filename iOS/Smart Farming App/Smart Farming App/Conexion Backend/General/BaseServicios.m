//
//  BaseServicios.m
//  Smart Farming App
//
//  Created by Facundo José Palma on 9/21/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "BaseServicios.h"

@implementation BaseServicios

#pragma mark - Publico

+(id)armarRespuestaServicio:(RespuestaServicioBase *)respuesta withResponseObject:(NSDictionary *)responseObject {
    
    if ([responseObject objectForKey:KEY_RESULTADO_OPERACION] != [NSNull null])  {
        NSString *resultado = [responseObject objectForKey:KEY_RESULTADO_OPERACION];
        if (resultado) {
            respuesta.resultado = [resultado boolValue];
        }
    }
    
    if ([responseObject objectForKey:KEY_DETALLE_OPERACION] != [NSNull null]) {
        respuesta.detalleOperacion = [responseObject objectForKey:KEY_DETALLE_OPERACION];
    }
    
    return [responseObject objectForKey:KEY_DATOS_OPERACION];
}

+(ErrorServicioBase*)armarErrorServicio:(NSError*)error {
    if ([error isKindOfClass:[ErrorServicioBase class]]) {
        ErrorServicioBase *errorServicio = (ErrorServicioBase*)error;
        return errorServicio;
    } else {
        return nil;
    }
}

@end
