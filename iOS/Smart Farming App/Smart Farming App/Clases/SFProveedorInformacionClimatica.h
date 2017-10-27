//
//  SFProveedorInformacionClimatica.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/24/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <Foundation/Foundation.h>

#import "SFTipoMedicionClimatica.h"

@interface SFProveedorInformacionClimatica : NSObject

@property (strong, nonatomic) NSString *nombreProveedor;
@property (strong, nonatomic) NSString *urlApi;

@property (strong, nonatomic) NSDate *fechaAltaProveedorFinca;

@property (assign, nonatomic) NSInteger frecuenciaMaximaPosible;
@property (assign, nonatomic) NSInteger frecuenciaActual;

@property (strong, nonatomic) NSArray<SFTipoMedicionClimatica*> *listaTipoMedicion;

@end
