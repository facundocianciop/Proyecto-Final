//
//  SFMedicionInformacionClimaticaCabecera.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/25/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <Foundation/Foundation.h>

#import "SFMedicionInformacionClimaticaDetalle.h"

@interface SFMedicionInformacionClimaticaCabecera : NSObject

@property (assign, nonatomic) NSInteger nroMedicion; // nroMedicion
@property (strong, nonatomic) NSDate *fechaYHora; // fechaHora

@property (strong, nonatomic) NSString *nombreProveedor; // proveedorInformacion

@property (strong, nonatomic) NSArray<SFMedicionInformacionClimaticaDetalle*> *listaDetallesMedicionInformacionClimatica; // mediciones_detalles

@end
