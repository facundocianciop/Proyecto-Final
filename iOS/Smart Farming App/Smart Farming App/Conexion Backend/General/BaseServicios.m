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

+(ErrorServicioBase*)armarErrorServicio:(NSError*)error {
    if ([error isKindOfClass:[ErrorServicioBase class]]) {
        ErrorServicioBase *errorServicio = (ErrorServicioBase*)error;
        return errorServicio;
    } else {
        return nil;
    }
}

@end
