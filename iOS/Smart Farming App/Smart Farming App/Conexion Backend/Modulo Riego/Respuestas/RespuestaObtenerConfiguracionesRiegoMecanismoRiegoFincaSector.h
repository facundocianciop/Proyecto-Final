//
//  RespuestaObtenerConfiguracionesRiegoMecanismoRiegoFincaSector.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/23/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "RespuestaServicioBase.h"
#import "SFConfiguracionRiego.h"

@interface RespuestaObtenerConfiguracionesRiegoMecanismoRiegoFincaSector : RespuestaServicioBase

@property (strong, nonatomic) NSArray<SFConfiguracionRiego*> *configuracionesRiego;

@end
