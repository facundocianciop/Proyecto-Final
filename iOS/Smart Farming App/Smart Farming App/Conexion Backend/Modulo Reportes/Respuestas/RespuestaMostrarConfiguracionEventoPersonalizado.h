//
//  RespuestaMostrarConfiguracionEventoPersonalizado.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/24/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "RespuestaServicioBase.h"

#import "SFConfiguracionEvento.h"

@interface RespuestaMostrarConfiguracionEventoPersonalizado : RespuestaServicioBase

@property (strong, nonatomic) SFConfiguracionEvento *configuracionEvento;

@end
