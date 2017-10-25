//
//  RespuestaObtenerEstadoActualSector.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/24/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "RespuestaServicioBase.h"

#import "SFComponenteSensor.h"
#import "SFMecanismoRiegoFincaSector.h"
#import "SFMedicionSensorCabecera.h"
#import "SFEjecucionRiego.h"
#import "SFConfiguracionRiego.h"

@interface RespuestaObtenerEstadoActualSector : RespuestaServicioBase

@property (assign, nonatomic) long idSector; // id_sector

@property (assign, nonatomic) NSInteger nroSector; // numero_sector
@property (strong, nonatomic) NSString *descripcionSector; // descripcion_sector

@property (assign, nonatomic) CGFloat superficieSector; // superficie_sector

@property (strong, nonatomic) SFComponenteSensor *componenteSensorSector; // componente_sector
@property (strong, nonatomic) SFMecanismoRiegoFincaSector *mecanismoRiegoFincaSector; // mecanismo_sector

@property (strong, nonatomic) SFMedicionSensorCabecera *ultimaMedicion; // ultima_medicion
@property (strong, nonatomic) SFEjecucionRiego *ejecucionRiego; // ejecucion_riego
@property (strong, nonatomic) SFConfiguracionRiego *configuracionRiego; // configuracion_riego

@end
