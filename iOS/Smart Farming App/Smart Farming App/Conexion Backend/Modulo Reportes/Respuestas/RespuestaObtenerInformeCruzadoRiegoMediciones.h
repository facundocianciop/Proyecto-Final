//
//  RespuestaObtenerInformeCruzadoRiegoMediciones.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/24/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "RespuestaServicioBase.h"

#import "DTOInformeCruzadoRiegoMediciones.h"

@interface RespuestaObtenerInformeCruzadoRiegoMediciones : RespuestaServicioBase

@property (strong, nonatomic) NSArray<DTOInformeCruzadoRiegoMediciones*> *listaDatosCruzados;

@end
