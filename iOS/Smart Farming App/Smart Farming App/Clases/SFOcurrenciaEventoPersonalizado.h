//
//  SFOcurrenciaEventoPersonalizado.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/25/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface SFOcurrenciaEventoPersonalizado : NSObject

@property (assign, nonatomic) NSInteger nroEvento; // nroEvento
@property (assign, nonatomic) NSInteger numeroSector; // numeroSector

@property (strong, nonatomic) NSDate *fechaYHora; // fechaHora

@end
