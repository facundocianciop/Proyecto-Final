//
//  SFConjuntoPermisos.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/24/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface SFConjuntoPermisos : NSObject

@property (assign, nonatomic) BOOL puedeAsignarComponenteSensor;
@property (assign, nonatomic) BOOL puedeAsignarCultivo;
@property (assign, nonatomic) BOOL puedeAsignarMecRiegoAFinca;
@property (assign, nonatomic) BOOL puedeAsignarMecRiegoASector;
@property (assign, nonatomic) BOOL puedeConfigurarObtencionInfoExterna;
@property (assign, nonatomic) BOOL puedeCrearComponenteSensor;
@property (assign, nonatomic) BOOL puedeCrearConfiguracionRiego;
@property (assign, nonatomic) BOOL puedeCrearSector;
@property (assign, nonatomic) BOOL puedeGenerarInformeCruzadoRiegoMedicion;
@property (assign, nonatomic) BOOL puedeGenerarInformeEstadoActualSectores;
@property (assign, nonatomic) BOOL puedeGenerarInformeEstadoHistoricoSectoresFinca;
@property (assign, nonatomic) BOOL puedeGenerarInformeEventoPersonalizado;
@property (assign, nonatomic) BOOL puedeGenerarInformeHeladasHistorico;
@property (assign, nonatomic) BOOL puedeGenerarInformeRiegoEnEjecucion;
@property (assign, nonatomic) BOOL puedeGenerarInformeRiegoPorSectoresHistorico;
@property (assign, nonatomic) BOOL puedeGestionarComponenteSensor;
@property (assign, nonatomic) BOOL puedeGestionarCultivoSector;
@property (assign, nonatomic) BOOL puedeGestionarEventoPersonalizado;
@property (assign, nonatomic) BOOL puedeGestionarFinca;
@property (assign, nonatomic) BOOL puedeGestionarSector;
@property (assign, nonatomic) BOOL puedeGestionarSensores;
@property (assign, nonatomic) BOOL puedeGestionarUsuariosFinca;
@property (assign, nonatomic) BOOL puedeIniciarODetenerRiegoManualmente;
@property (assign, nonatomic) BOOL puedeModificarConfiguracionRiego;

@end
