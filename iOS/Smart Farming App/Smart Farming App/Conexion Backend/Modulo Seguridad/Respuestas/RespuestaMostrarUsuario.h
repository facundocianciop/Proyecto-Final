//
//  RespuestaMostrarUsuario.h
//  Smart Farming App
//
//  Created by Facundo Palma on 10/16/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "RespuestaServicioBase.h"

@interface RespuestaMostrarUsuario : RespuestaServicioBase

@property (strong, nonatomic) NSString *username;
@property (strong, nonatomic) NSString *email;

@property (strong, nonatomic) NSString *nombre;
@property (strong, nonatomic) NSString *apellido;

@property (strong, nonatomic) NSDate *fechaNacimiento;
@property (assign, nonatomic) NSInteger dni;
@property (strong, nonatomic) NSString *cuit;
@property (strong, nonatomic) NSString *domicilio;

@end
