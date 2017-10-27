//
//  ServiciosModuloSectores.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/18/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "BaseServicios.h"

#import "SolicitudMostrarSectores.h"
#import "RespuestaMostrarSectores.h"

#import "SolicitudBuscarSectorId.h"
#import "RespuestaBuscarSectorId.h"

#import "SolicitudMostrarCultivoSector.h"
#import "RespuestaMostrarCultivoSector.h"

#import "SolicitudMostrarCultivoSectorHistorico.h"
#import "RespuestaMostrarCultivoSectorHistorico.h"

#import "SolicitudMostrarMecanismoRiegoSector.h"
#import "RespuestaMostrarMecanismoRiegoSector.h"

#import "SolcitudMostrarComponenteSensorSector.h"
#import "RespuestaMostrarComponenteSensorSector.h"

@interface ServiciosModuloSectores : BaseServicios

+(void) mostrarSectores:(SolicitudMostrarSectores*)solicitudMostrarSectores completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock;

+(void) buscarSectorId:(SolicitudBuscarSectorId*)solicitudBuscarSectorId completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock;

+(void) mostrarCultivoSector:(SolicitudMostrarCultivoSector*)solicitudMostrarCultivoSector
             completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock;

+(void) mostrarCultivoSectorHistorico:(SolicitudMostrarCultivoSectorHistorico*)solicitudMostrarCultivoSectorHistorico completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock;

+(void) mostrarMecanismoRiegoSector:(SolicitudMostrarMecanismoRiegoSector*)solicitudMostrarMecanismoRiegoSector completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock;

+(void) mostrarComponenteSensorSector:(SolcitudMostrarComponenteSensorSector*)solcitudMostrarComponenteSensorSector completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock;

@end
