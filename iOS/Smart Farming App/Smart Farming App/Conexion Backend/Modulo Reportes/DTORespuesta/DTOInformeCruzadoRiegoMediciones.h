//
//  DTOInformeCruzadoRiegoMediciones.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/25/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <Foundation/Foundation.h>

#import "SFMecanismoRiegoFincaSector.h"
#import "SFEjecucionRiego.h"
#import "SFConfiguracionRiego.h"
#import "SFMedicionSensorCabecera.h"
#import "SFMedicionInformacionClimaticaCabecera.h"


@interface DTOInformeCruzadoRiegoMediciones : NSObject

@property (strong, nonatomic) SFMecanismoRiegoFincaSector *mecanismoRiegoFincaSector; // mecanismo_riego_finca_sector
@property (strong, nonatomic) SFEjecucionRiego *ejecucionRiego; // ejecucion
@property (strong, nonatomic) SFConfiguracionRiego *configuracionRiego; // configuracion

@property (strong, nonatomic) NSArray<SFMedicionSensorCabecera*> *medicionesComponenteAntes; // medicionesComponenteAntes
@property (strong, nonatomic) NSArray<SFMedicionSensorCabecera*> *medicionesComponenteDespues; // medicionesComponenteDespues

@property (strong, nonatomic) NSArray<SFMedicionInformacionClimaticaCabecera*> *medicionesClimaticasAntes; // medicionesClimaticasAntes

@end
