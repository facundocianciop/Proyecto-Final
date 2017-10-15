//
//  RespuestaInicioSesion.h
//  Smart Farming App
//
//  Created by Facundo Palma on 10/13/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "RespuestaServicioBase.h"

@interface RespuestaInicioSesion : RespuestaServicioBase

@property (strong, nonatomic) NSString *username;
@property (strong, nonatomic) NSString *nombre;
@property (strong, nonatomic) NSString *apellido;

@end
