//
//  SFFinca.h
//  Smart Farming App
//
//  Created by Facundo Palma on 10/14/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface SFFinca : NSObject

@property (assign, nonatomic) long idFinca;
@property (strong, nonatomic) NSString *nombre;

@property (assign, nonatomic) NSInteger tamanio;
@property (strong, nonatomic) NSString *ubicacion;
@property (strong, nonatomic) NSString *direccionLegal;

@end
