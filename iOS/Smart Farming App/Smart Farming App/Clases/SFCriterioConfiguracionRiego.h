//
//  SFCriterioConfiguracionRiego.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/25/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <UIKit/UIKit.h>

@interface SFCriterioConfiguracionRiego : NSObject

@property (assign, nonatomic) long idCriterioRiego; // id_criterio_riego

@property (strong, nonatomic) NSString *nombreTipoCriterioRiego; // tipo_criterio_riego

@property (strong, nonatomic) NSString *nombreCriterioRiego; // nombre
@property (strong, nonatomic) NSString *descripcionCriterioRiego; // descripcion

@property (strong, nonatomic) NSDate *fechaCreacionCriterio; // fechaCreacionCriterio

@end
