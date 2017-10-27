//
//  SFCriterioConfiguracionRiegoHora.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/25/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFCriterioConfiguracionRiego.h"

@interface SFCriterioConfiguracionRiegoHora : SFCriterioConfiguracionRiego

@property (strong, nonatomic) NSString *hora; // hora
@property (assign, nonatomic) NSInteger numeroDia; // numeroDia

@end
