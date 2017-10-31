//
//  IdentificadoresSegue.m
//  Smart Farming App
//
//  Created by Facundo Palma on 10/12/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "IdentificadoresSegue.h"

@implementation IdentificadoresSegue

#pragma mark - Modulo Seguridad

NSString *const kSFNavegarEstadoAutenticadoSegue = @"SFNavegarEstadoAutenticadoSegue";
NSString *const kSFNavegarEstadoNoAutenticadoSegue = @"SFNavegarEstadoNoAutenticadoSegue";

NSString *const kSFNavegarRecuperarCuentaSegundoPaso = @"SFNavegarRecuperarCuentaSegundoPaso";

NSString *const kSFNavegarModificarUsuarioSegue = @"SFNavegarModificarUsuarioSegue";

#pragma mark - Modulo Finca

NSString *const kSFNavegarASeccionFincaSegue = @"SFNavegarASeccionFincaSegue";

NSString *const kSFNavegarASectoresFincaSegue = @"SFNavegarASectoresFincaSegue";
NSString *const kSFNavegarASensoresFincaSegue = @"SFNavegarASensoresFincaSegue";
NSString *const kSFNavegarAConfiguracionEventoSegue = @"SFNavegarAConfiguracionEventoSegue";
NSString *const kSFNavegarAMecanismosRiegoFincaSegue = @"SFNavegarAMecanismosRiegoFincaSegue";
NSString *const kSFNavegarReportesFincaSegue = @"SFNavegarReportesFincaSegue";

#pragma mark - Modulo Sectores

NSString *const kSFNavegarAInfoSectorSegue = @"SFNavegarAInfoSectorSegue";

NSString *const kSFNavegarAInfoCultivoSectorSegue = @"SFNavegarAInfoCultivoSectorSegue";
NSString *const kSFNavegarAInfoMecanismoRiegoSectorSegue = @"SFNavegarAInfoMecanismoRiegoSectorSegue";
NSString *const kSFNavegarAInfoComponenteSensorSector = @"SFNavegarAInfoComponenteSensorSector";

NSString *const kSFNavegarConfiguracionesRiegoSegue = @"SFNavegarConfiguracionesRiegoSegue";
NSString *const kSFNavegarCriteriosRiegoSegue = @"SFNavegarCriteriosRiegoSegue";

#pragma mark - Modulo Riego

NSString *const kSFNavegarInfoEjecucionRiego = @"SFNavegarInfoEjecucionRiego";

#pragma mark - Modulo Reportes - Configuracion eventos

NSString *const kSFNavegarAMedicionesConfiguracionEvento = @"SFNavegarAMedicionesConfiguracionEvento";

#pragma mark - Modulo Reportes

NSString *const kSFNavegarAReporteEstadoSectorSegue = @"SFNavegarAReporteEstadoSectorSegue";
NSString *const kSFNavegarAReporteEventosPersonalizadosSegue = @"SFNavegarAReporteEventosPersonalizadosSegue";
NSString *const kSFNavegarAReporteHeladasSegue = @"SFNavegarAReporteHeladasSegue";
NSString *const kSFNavegarAReporteRiegoEnEjecucionSegue = @"SFNavegarAReporteRiegoEnEjecucionSegue";

NSString *const kSFNavegarAReporteEstadoSectorDetalleSegue = @"SFNavegarAReporteEstadoSectorDetalleSegue";
NSString *const kSFNavegarAReporteEstadoActualEjecucionSegue = @"SFNavegarAReporteEstadoActualEjecucionSegue";
NSString *const kSFNavegarAReporteEstadoActualMedicionSegue = @"SFNavegarAReporteEstadoActualMedicionSegue";

NSString *const kSFNavegarAReporteEventosPersonalizadosConfiguracionSegue = @"SFNavegarAReporteEventosPersonalizadosConfiguracionSegue";
NSString *const kSFNavegarAReporteEventosPersonalizadosRegistradosSegue = @"SFNavegarAReporteEventosPersonalizadosRegistradosSegue";

NSString *const kSFNavegarAReporteHeladasSeleccionarFechaSegue = @"SFNavegarAReporteHeladasSeleccionarFechaSegue";
NSString *const kSFNavegarAReporteHeladasEventosSegue = @"SFNavegarAReporteHeladasEventosSegue";

@end
