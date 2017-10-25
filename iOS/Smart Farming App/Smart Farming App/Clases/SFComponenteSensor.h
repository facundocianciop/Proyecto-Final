//
//  SFComponenteSensor.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/23/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface SFComponenteSensor : NSObject

@property (assign, nonatomic) long idComponenteSensor; // idComponenteSensor
@property (assign, nonatomic) long idFinca; // finca

@property (strong, nonatomic) NSString *modelo; // modelo
@property (strong, nonatomic) NSString *descripcion; // descripcion

@property (strong, nonatomic) NSString *estadoComponenteSensor; // estado

@property (assign, nonatomic) NSInteger cantidadMaximaSensores; // cantidadMaximaSensores
@property (assign, nonatomic) NSInteger cantidadSensoresAsignados; // cantidadSensoresAsignados

@end
