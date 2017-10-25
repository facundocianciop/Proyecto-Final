//
//  SFEjecucionRiego.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/25/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <UIKit/UIKit.h>

@interface SFEjecucionRiego : NSObject

@property (assign, nonatomic) long idMecanismoRiegoFincaSector; // mecanismoRiegoFincaSector
@property (assign, nonatomic) long idConfiguracionRiego; // configuracion_riego

@property (strong, nonatomic) NSString *nombreEstadoEjecucionRiego; // estado_ejecucion_riego
@property (strong, nonatomic) NSString *detalle; // detalle

@property (assign, nonatomic) CGFloat cantidadAguaUtilizadaLitros; // cantidadAguaUtilizadaLitros

@property (assign, nonatomic) CGFloat duracionActualMinutos; // duracionActualMinutos
@property (assign, nonatomic) CGFloat duracionActualSegundos; // duracionActualSegundos

@property (strong, nonatomic) NSDate *fechaHoraFinalizacion; // fechaHoraFinalizacion
@property (strong, nonatomic) NSDate *fechaHoraFinalProgramada; // fechaHoraFinalProgramada

@property (strong, nonatomic) NSDate *fechaHoraInicio; // fechaHoraInicio
@property (strong, nonatomic) NSDate *fechaHoraInicioProgramada; // fechaHoraInicioProgramada

@end
