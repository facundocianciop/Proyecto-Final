//
//  ServiciosModuloSensores.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/24/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "BaseServicios.h"

#import "SolicitudMostrarComponentesSensorFinca.h"
#import "RespuestaMostrarComponentesSensorFinca.h"

#import "SolicitudMostrarComponentesSensorFincaHabilitados.h"
#import "RespuestaMostrarComponentesSensorFincaHabilitados.h"

#import "RespuestaMostrarTipoMedicion.h"

#import "SolicitudMostrarSensoresFinca.h"
#import "RespuestaMostrarSensoresFinca.h"

@interface ServiciosModuloSensores : BaseServicios

+(void) mostrarComponentesSensorFinca:(SolicitudMostrarComponentesSensorFinca*)solicitudMostrarComponentesSensorFinca completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock;

+(void) mostrarComponentesSensorFincaHabilitados:(SolicitudMostrarComponentesSensorFincaHabilitados*)solicitudMostrarComponentesSensorFincaHabilitados completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock;

+(void) mostrarTipoMedicion:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock;

+(void) mostrarSensoresFinca:(SolicitudMostrarSensoresFinca*)solicitudMostrarSensoresFinca completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock;

@end
