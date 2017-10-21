//
//  SolicitudRecuperarCuentaCambiarContrasenia.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/19/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SolicitudServicioBase.h"

@interface SolicitudRecuperarCuentaCambiarContrasenia : SolicitudServicioBase

@property (strong, nonatomic) NSString *username;
@property (strong, nonatomic) NSString *codigoVerificacion;
@property (strong, nonatomic) NSString *contraseniaNueva;

@end
