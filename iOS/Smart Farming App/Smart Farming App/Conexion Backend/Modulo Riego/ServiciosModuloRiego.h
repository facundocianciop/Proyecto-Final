//
//  ServiciosModuloRiego.h
//  Smart Farming App
//
//  Created by Facundo Palma on 10/13/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "BaseServicios.h"

#import "SolicitudObtenerRiegoEnEjecucionMecanismoRiegoFincaSector.h"
#import "RespuestaObtenerRiegoEnEjecucionMecanismoRiegoFincaSector.h"

#import "SolicitudIniciarRiegoManualmente.h"
#import "RespuestaIniciarRiegoManualmente.h"

#import "SolicitudPausarRiegoManualmente.h"
#import "RespuestaPausarRiegoManualmente.h"

#import "SolicitudCancelarRiegoManualmente.h"
#import "RespuestaCancelarRiegoManualmente.h"

#import "SolicitudObtenerConfiguracionesRiegoMecanismoRiegoFincaSector.h"
#import "RespuestaObtenerConfiguracionesRiegoMecanismoRiegoFincaSector.h"

#import "SolicitudObtenerCriteriosInicialesConfiguracionRiegoMecanismoRiegoFincaSector.h"
#import "RespuestaObtenerCriteriosInicialesConfiguracionRiegoMecanismoRiegoFincaSector.h"

#import "SolicitudObtenerCriteriosFinalesConfiguracionRiegoMecanismoRiegoFincaSector.h"
#import "RespuestaObtenerCriteriosFinalesConfiguracionRiegoMecanismoRiegoFincaSector.h"

@interface ServiciosModuloRiego : BaseServicios

+(void) obtenerRiegoEnEjecucionMecanismoRiegoFincaSector:(SolicitudObtenerRiegoEnEjecucionMecanismoRiegoFincaSector*)solicitudObtenerRiegoEnEjecucionMecanismoRiegoFincaSector completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock;

+(void) iniciarRiegoManualmente:(SolicitudIniciarRiegoManualmente*)solicitudIniciarRiegoManualmente completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock;

+(void) pausarRiegoManualmente:(SolicitudPausarRiegoManualmente*)solicitudPausarRiegoManualmente completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock;

+(void) cancelarRiegoManualmente:(SolicitudCancelarRiegoManualmente*)solicitudCancelarRiegoManualmente completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock;

+(void) obtenerConfiguracionesRiegoMecanismoRiegoFincaSector:(SolicitudObtenerConfiguracionesRiegoMecanismoRiegoFincaSector*)solicitudObtenerConfiguracionesRiegoMecanismoRiegoFincaSector completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock;

+(void) obtenerCriteriosInicialesConfiguracionRiegoMecanismoRiegoFincaSector:(SolicitudObtenerCriteriosInicialesConfiguracionRiegoMecanismoRiegoFincaSector*)solicitudObtenerCriteriosInicialesConfiguracionRiegoMecanismoRiegoFincaSector completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock;

+(void) obtenerCriteriosFinalesConfiguracionRiegoMecanismoRiegoFincaSector:(SolicitudObtenerCriteriosFinalesConfiguracionRiegoMecanismoRiegoFincaSector*)solicitudObtenerCriteriosFinalesConfiguracionRiegoMecanismoRiegoFincaSector completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock;

@end
