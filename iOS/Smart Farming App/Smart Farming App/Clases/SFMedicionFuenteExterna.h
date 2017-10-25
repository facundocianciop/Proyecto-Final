//
//  SFMedicionFuenteExterna.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/25/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <UIKit/UIKit.h>

@interface SFMedicionFuenteExterna : NSObject

@property (strong, nonatomic) NSString *nombreTipoMedicion; // tipo_medicion
@property (strong, nonatomic) NSString *unidadMedicion; // unidad_medicion

@property (assign, nonatomic) CGFloat valorMaximo; // valor_maximo
@property (assign, nonatomic) CGFloat valorMinimo; // valor_minimo

@end
