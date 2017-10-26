//
//  RespuestaObtenerCriteriosInicialesConfiguracionRiegoMecanismoRiegoFincaSector.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/23/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "RespuestaServicioBase.h"

#import "SFCriterioConfiguracionRiego.h"
#import "SFCriterioConfiguracionRiegoHora.h"
#import "SFCriterioConfiguracionRiegoVolumenAgua.h"
#import "SFCriterioConfiguracionRiegoMedicion.h"

@interface RespuestaObtenerCriteriosInicialesConfiguracionRiegoMecanismoRiegoFincaSector : RespuestaServicioBase

@property (strong, nonatomic) NSArray<SFCriterioConfiguracionRiego*> *criteriosInicialesConfiguracionRiego;

@end
