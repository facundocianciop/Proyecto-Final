//
//  RespuestaMostrarCultivoSector.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/23/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "RespuestaServicioBase.h"

#import "SFCultivoSector.h"

@interface RespuestaMostrarCultivoSector : RespuestaServicioBase

@property (strong, nonatomic) SFCultivoSector *cultivoSector;

@end
