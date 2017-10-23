//
//  SFMecanismoRiegoFincaSector.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/18/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface SFMecanismoRiegoFincaSector : NSObject

@property (assign, nonatomic) long idMecanismoRiegoFincaSector;

@property (assign, nonatomic) long idFinca;
@property (assign, nonatomic) long idMecanismoRiegoFinca;
@property (assign, nonatomic) long idSector;

@property (strong, nonatomic) NSString *nombreTipoMecanismo;

@property (assign, nonatomic) CGFloat caudal;
@property (assign, nonatomic) CGFloat presion;

@end
