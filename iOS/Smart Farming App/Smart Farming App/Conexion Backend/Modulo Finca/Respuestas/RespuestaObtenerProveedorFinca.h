//
//  RespuestaObtenerProveedorFinca.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/24/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "RespuestaServicioBase.h"

#import "SFProveedorInformacionClimatica.h"

@interface RespuestaObtenerProveedorFinca : RespuestaServicioBase

@property (strong, nonatomic) SFProveedorInformacionClimatica *proveedorInformacionClimatica;

@end
