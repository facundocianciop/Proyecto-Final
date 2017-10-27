//
//  SFTipoMedicionClimatica.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/24/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface SFTipoMedicionClimatica : NSObject

@property (assign, nonatomic) long idTipoMedicionClimatica;

@property (strong, nonatomic) NSString *nombreTipoMedicionClimatica;
@property (strong, nonatomic) NSString *unidadMedicion;

@property (strong, nonatomic) NSDate *fechaAltaTipoMedicionClimatica;
@property (strong, nonatomic) NSDate *fechaBajaTipoMedicionClimatica;

@property (assign, nonatomic) BOOL habilitada;

@end
