//
//  SFCultivoSector.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/23/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface SFCultivoSector : NSObject

@property (assign, nonatomic) long idCultivoSector;

@property (strong, nonatomic) NSString *nombreCultivoSector;
@property (strong, nonatomic) NSString *descripcionCultivoSector;

@property (strong, nonatomic) NSString *subTipoCultivo;
@property (strong, nonatomic) NSString *tipoCultivo;

@property (strong, nonatomic) NSDate *fechaPlantacionCultivoSector;
@property (strong, nonatomic) NSDate *fechaEliminacionCultivoSector;

@property (assign, nonatomic) BOOL habilitado;

@end
