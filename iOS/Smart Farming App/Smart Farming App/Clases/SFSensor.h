//
//  SFSensor.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/25/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <Foundation/Foundation.h>

#import "SFTipoMedicion.h"

@interface SFSensor : NSObject

@property (assign, nonatomic) long idSensor; // idSensor

@property (strong, nonatomic) NSString *nombreTipoMedicion; // tipoMedicion
@property (strong, nonatomic) NSString *modelo; // modelo

@property (strong, nonatomic) NSDate *fechaAltaSensor; // fechaAltaSensor
@property (strong, nonatomic) NSDate *fechaBajaSensor; // fechaBajaSensor

@property (assign, nonatomic) BOOL habilitado; // habilitado

@end
