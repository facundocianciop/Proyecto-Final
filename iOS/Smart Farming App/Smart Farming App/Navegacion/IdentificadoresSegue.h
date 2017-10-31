//
//  IdentificadoresSegue.h
//  Smart Farming App
//
//  Created by Facundo Palma on 10/12/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface IdentificadoresSegue : NSObject

#pragma mark - Modulo Seguridad

extern NSString *const kSFNavegarEstadoAutenticadoSegue;
extern NSString *const kSFNavegarEstadoNoAutenticadoSegue;

extern NSString *const kSFNavegarRecuperarCuentaSegundoPaso;

extern NSString *const kSFNavegarModificarUsuarioSegue;

#pragma mark - Modulo Finca

extern NSString *const kSFNavegarASeccionFincaSegue;

extern NSString *const kSFNavegarASectoresFincaSegue;
extern NSString *const kSFNavegarASensoresFincaSegue;
extern NSString *const kSFNavegarAConfiguracionEventoSegue;
extern NSString *const kSFNavegarAMecanismosRiegoFincaSegue;
extern NSString *const kSFNavegarReportesFincaSegue;

#pragma mark - Modulo Sectores

extern NSString *const kSFNavegarAInfoSectorSegue;
extern NSString *const kSFNavegarAInfoMecanismoRiegoSectorSegue;

extern NSString *const kSFNavegarAInfoCultivoSectorSegue;
extern NSString *const kSFNavegarAInfoMecanismoRiegoSectorSegue;
extern NSString *const kSFNavegarAInfoComponenteSensorSector;

extern NSString *const kSFNavegarConfiguracionesRiegoSegue;
extern NSString *const kSFNavegarCriteriosRiegoSegue;

#pragma mark - Modulo Sensores


#pragma mark - Modulo Riego

extern NSString *const kSFNavegarInfoEjecucionRiego;

#pragma mark - Modulo Reportes - Configuracion eventos

extern NSString *const kSFNavegarAMedicionesConfiguracionEvento;

#pragma mark - Modulo Reportes

extern NSString *const kSFNavegarAReporteEstadoSectorSegue;
extern NSString *const kSFNavegarAReporteEventosPersonalizadosSegue;
extern NSString *const kSFNavegarAReporteHeladasSegue;
extern NSString *const kSFNavegarAReporteRiegoEnEjecucionSegue;


extern NSString *const kSFNavegarAReporteEstadoSectorDetalleSegue;
extern NSString *const kSFNavegarAReporteEstadoActualEjecucionSegue;
extern NSString *const kSFNavegarAReporteEstadoActualMedicionSegue;

extern NSString *const kSFNavegarAReporteEventosPersonalizadosConfiguracionSegue;
extern NSString *const kSFNavegarAReporteEventosPersonalizadosRegistradosSegue;

extern NSString *const kSFNavegarAReporteHeladasSeleccionarFechaSegue;
extern NSString *const kSFNavegarAReporteHeladasEventosSegue;

@end
