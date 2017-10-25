//
//  ServiciosModuloReportes.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/24/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "BaseServicios.h"

#import "SolicitudBuscarConfiguracionesEventosPersonalizados.h"
#import "RespuestaBuscarConfiguracionesEventosPersonalizados.h"

#import "SolicitudMostrarConfiguracionEventoPersonalizado.h"
#import "RespuestaMostrarConfiguracionEventoPersonalizado.h"

#import "SolicitudObtenerEstadoActualSector.h"
#import "RespuestaObtenerEstadoActualSector.h"

#import "SolicitudObtenerInformeHistoricoSector.h"
#import "RespuestaObtenerInformeHistoricoSector.h"

#import "SolicitudObtenerInformeRiegoEjecucionSector.h"
#import "RespuestaObtenerInformeRiegoEjecucionSector.h"

#import "SolicitudObtenerInformeRiegoHistoricoSector.h"
#import "RespuestaObtenerInformeRiegoHistoricoSector.h"

#import "SolicitudObtenerInformeEventosPersonalizados.h"
#import "RespuestaObtenerInformeEventosPersonalizados.h"

#import "SolicitudObtenerInformeHistoricoHeladas.h"
#import "RespuestaObtenerInformeHistoricoHeladas.h"

#import "SolicitudObtenerInformeCruzadoRiegoMediciones.h"
#import "RespuestaObtenerInformeCruzadoRiegoMediciones.h"

@interface ServiciosModuloReportes : BaseServicios

+(void) buscarConfiguracionesEventosPersonalizados:(SolicitudBuscarConfiguracionesEventosPersonalizados*)solicitudBuscarConfiguracionesEventosPersonalizados completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock;

+(void) mostrarConfiguracionEventoPersonalizado:(SolicitudMostrarConfiguracionEventoPersonalizado*)solicitudMostrarConfiguracionEventoPersonalizado completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock;

+(void) obtenerEstadoActualSector:(SolicitudObtenerEstadoActualSector*)solicitudObtenerEstadoActualSector completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock;

+(void) obtenerInformeHistoricoSector:(SolicitudObtenerInformeHistoricoSector*)solicitudObtenerInformeHistoricoSector completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock;

+(void) obtenerInformeRiegoEjecucionSector:(SolicitudObtenerInformeRiegoEjecucionSector*)solicitudObtenerInformeRiegoEjecucionSector completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock;

+(void) obtenerInformeRiegoHistoricoSector:(SolicitudObtenerInformeRiegoHistoricoSector*)solicitudObtenerInformeRiegoHistoricoSector completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock;

+(void) obtenerInformeEventosPersonalizados:(SolicitudObtenerInformeEventosPersonalizados*)solicitudObtenerInformeEventosPersonalizados completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock;

+(void) obtenerInformeHistoricoHeladas:(SolicitudObtenerInformeHistoricoHeladas*)solicitudObtenerInformeHistoricoHeladas completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock;

+(void) obtenerInformeCruzadoRiegoMediciones:(SolicitudObtenerInformeCruzadoRiegoMediciones*)solicitudObtenerInformeCruzadoRiegoMediciones completionBlock:(SuccessBlock)completionBlock failureBlock:(FailureBlock)failureBlock;

@end
