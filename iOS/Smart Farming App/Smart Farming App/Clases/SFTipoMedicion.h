//
//  SFTipoMedicion.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/25/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface SFTipoMedicion : NSObject

@property (assign, nonatomic) long idTipoMedicion; // idTipoMedicion

@property (strong, nonatomic) NSString *nombreTipoMedicion; // nombreTipoMedicion
@property (strong, nonatomic) NSString *unidadMedicion; // unidadMedicion

@property (strong, nonatomic) NSDate *fechaAltaTipoMedicion; // fechaAltaTipoMedicion
@property (strong, nonatomic) NSDate *fechaBajaTipoMedicion; // fechaBajaTipoMedicion

@property (assign, nonatomic) BOOL habilitado; // habilitado

@end
