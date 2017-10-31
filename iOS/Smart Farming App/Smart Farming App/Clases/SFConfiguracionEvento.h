//
//  SFConfiguracionEvento.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/25/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <Foundation/Foundation.h>

#import "SFMedicionFuenteInterna.h"
#import "SFMedicionFuenteExterna.h"

@interface SFConfiguracionEvento : NSObject

@property (assign, nonatomic) long idUsuarioFinca; // id_usuario_finca
@property (assign, nonatomic) long idConfiguracionEvento; // id_configuracion_evento

@property (assign, nonatomic) long idSector; // id_sector

@property (strong, nonatomic) NSString *nombreConfiguracioEvento; // nombre
@property (strong, nonatomic) NSString *descripcionConfiguracioEvento; // descripcion

@property (strong, nonatomic) NSDate *fechaHoraCreacion; // fecha_hora_creacion

@property (assign, nonatomic) BOOL activado; // activado
@property (assign, nonatomic) BOOL notificacionActivada; // notificacion_activada

@property (strong, nonatomic) NSArray<SFMedicionFuenteInterna*> *listaMedicionesInternas; // lista_mediciones_internas
@property (strong, nonatomic) NSArray<SFMedicionFuenteExterna*> *listaMedicionesExternas; // lista_mediciones_externas

@end
