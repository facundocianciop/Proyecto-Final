//
//  RespuestaMostrarFincas.h
//  Smart Farming App
//
//  Created by Facundo Palma on 10/13/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "RespuestaServicioBase.h"
#import "SFFinca.h"

@interface RespuestaMostrarFincas : RespuestaServicioBase

@property (strong, nonatomic) NSArray<SFFinca*> *fincas;

@end
