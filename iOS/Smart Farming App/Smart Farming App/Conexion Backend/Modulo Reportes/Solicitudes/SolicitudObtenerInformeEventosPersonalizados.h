//
//  SolicitudObtenerInformeEventosPersonalizados.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/24/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SolicitudServicioBase.h"

@interface SolicitudObtenerInformeEventosPersonalizados : SolicitudServicioBase

@property (assign, nonatomic) long idFinca;
@property (assign, nonatomic) long idSector;
@property (assign, nonatomic) long idConfiguracionEvento;

@property (strong, nonatomic) NSDate *fechaInicioSector;
@property (strong, nonatomic) NSDate *fechaFinSector;

@end
