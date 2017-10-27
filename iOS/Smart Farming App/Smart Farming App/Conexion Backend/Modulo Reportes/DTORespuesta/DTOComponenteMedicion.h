//
//  DTOComponenteMedicion.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/25/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <Foundation/Foundation.h>

#import "SFComponenteSensor.h"
#import "SFMedicionSensorCabecera.h"

@interface DTOComponenteMedicion : NSObject

@property (strong, nonatomic) SFComponenteSensor *componenteSensor; //componente
@property (strong, nonatomic) SFMedicionSensorCabecera *medicionCabecera; //medicionCabecera

@end
