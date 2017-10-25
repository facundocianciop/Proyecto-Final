//
//  SolicitudObtenerInformeRiegoHistoricoSector.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/24/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SolicitudServicioBase.h"

@interface SolicitudObtenerInformeRiegoHistoricoSector : SolicitudServicioBase

@property (assign, nonatomic) long idFinca;
@property (assign, nonatomic) long idSector;

@property (strong, nonatomic) NSDate *fechaInicioSector;
@property (strong, nonatomic) NSDate *fechaFinSector;

@end
