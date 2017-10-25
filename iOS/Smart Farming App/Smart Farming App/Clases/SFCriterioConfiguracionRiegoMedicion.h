//
//  SFCriterioConfiguracionRiegoMedicion.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/25/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFCriterioConfiguracionRiego.h"

@interface SFCriterioConfiguracionRiegoMedicion : SFCriterioConfiguracionRiego

@property (strong, nonatomic) NSString *unidadMedicion; // unidadMedicion
@property (strong, nonatomic) NSString *nombreTipoMedicion; // tipoMedicion

@property (assign, nonatomic) CGFloat valor; // valor

@end
