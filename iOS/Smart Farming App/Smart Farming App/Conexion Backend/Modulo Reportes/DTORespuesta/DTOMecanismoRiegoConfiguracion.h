//
//  DTOMecanismoRiegoConfiguracion.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/27/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <Foundation/Foundation.h>

#import "SFMecanismoRiegoFincaSector.h"
#import "SFEjecucionRiego.h"
#import "SFConfiguracionRiego.h"

@interface DTOMecanismoRiegoConfiguracion : NSObject

@property (strong, nonatomic) SFMecanismoRiegoFincaSector *mecanismoRiegoFincaSector; // mecanismo_riego_finca_sector
@property (strong, nonatomic) SFEjecucionRiego *ejecucionRiego; // ejecucion
@property (strong, nonatomic) SFConfiguracionRiego *configuracionRiego; // configuracion

@end
