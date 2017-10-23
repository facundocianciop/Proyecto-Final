//
//  SFComponenteSensor.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/23/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface SFComponenteSensor : NSObject

@property (assign, nonatomic) long idComponenteSensor;
@property (assign, nonatomic) long idFinca;

@property (strong, nonatomic) NSString *modelo;
@property (strong, nonatomic) NSString *descripcion;

@property (strong, nonatomic) NSString *estadoComponenteSensor;

@property (assign, nonatomic) NSInteger cantidadMaximaSensores;
@property (assign, nonatomic) NSInteger cantidadSensoresAsignados;

@end
