//
//  SolicitudBuscarConfiguracionesEventosPersonalizados.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/24/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SolicitudServicioBase.h"

@interface SolicitudBuscarConfiguracionesEventosPersonalizados : SolicitudServicioBase

@property (assign, nonatomic) long idFinca;
@property (assign, nonatomic) long idUsuarioFinca;
@property (assign, nonatomic) long idSector;

@end
