//
//  SFMedicionSensorCabecera.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/25/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <Foundation/Foundation.h>

#import "SFMedicionSensorDetalle.h"

@interface SFMedicionSensorCabecera : NSObject

@property (assign, nonatomic) NSInteger nroMedicion; // nro_medicion
@property (strong, nonatomic) NSDate *fechaYHora; // fecha_y_hora

@property (strong, nonatomic) NSArray<SFMedicionSensorDetalle*> *listaDetallesMedicion; // lista_mediciones_detalle

@end
