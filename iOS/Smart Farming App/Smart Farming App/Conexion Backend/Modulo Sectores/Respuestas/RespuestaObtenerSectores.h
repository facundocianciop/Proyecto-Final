//
//  RespuestaObtenerSectores.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/18/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "RespuestaServicioBase.h"
#import "SFSectorFinca.h"

@interface RespuestaObtenerSectores : RespuestaServicioBase

@property (strong, nonatomic) NSArray<SFSectorFinca*> *sectores;

@end
