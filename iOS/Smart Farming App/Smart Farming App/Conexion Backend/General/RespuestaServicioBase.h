//
//  RespuestaServicioBase.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/11/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface RespuestaServicioBase : NSObject

@property (assign, nonatomic) BOOL resultado;
@property (strong, nonatomic) NSString *detalleOperacion;

@end
