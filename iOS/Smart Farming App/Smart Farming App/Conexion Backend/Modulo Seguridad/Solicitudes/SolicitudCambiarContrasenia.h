//
//  SolicitudCambiarContrasenia.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/19/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SolicitudServicioBase.h"

@interface SolicitudCambiarContrasenia : SolicitudServicioBase

@property (strong, nonatomic) NSString *contraseniaActual;
@property (strong, nonatomic) NSString *contraseniaNueva;

@end
