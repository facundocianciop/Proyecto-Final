//
//  SFConfiguracionRiego.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/25/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <UIKit/UIKit.h>

@interface SFConfiguracionRiego : NSObject

@property (assign, nonatomic) long idConfiguracionRiego; // idConfiguracionRiego
@property (assign, nonatomic) long idMecanismoRiegoFincaSector; // mecanismoRiegoFincaSector

@property (strong, nonatomic) NSString *nombreConfiguracionRiego; // nombre
@property (strong, nonatomic) NSString *descripcionConfiguracionRiego; // descripcion

@property (assign, nonatomic) CGFloat duracionMaxima; // duracionMaxima

@property (strong, nonatomic) NSDate *fechaCreacion; // fechaCreacion
@property (strong, nonatomic) NSDate *fechaFinalizacion; // fechaFinalizacion

@property (strong, nonatomic) NSString *nombreTipoConfiguracionRiego; // tipoConfiguracionRiego
@property (strong, nonatomic) NSString *nombreEstadoConfiguracionRiego; // estado_configuracion

@property (strong, nonatomic) NSDate *fechaHoraInicio; // fechaHoraInicio
@property (strong, nonatomic) NSDate *fechaHoraInicioProgramada; // fechaHoraInicioProgramada

@end
