//
//  SolicitudRegistrarUsuario.h
//  Smart Farming App
//
//  Created by Facundo Palma on 10/19/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SolicitudServicioBase.h"

@interface SolicitudRegistrarUsuario : SolicitudServicioBase

@property (strong, nonatomic) NSString *usuario;
@property (strong, nonatomic) NSString *email;
@property (strong, nonatomic) NSString *contrasenia;

@property (strong, nonatomic) NSString *nombre;
@property (strong, nonatomic) NSString *apellido;

@property (strong, nonatomic) NSDate *fechaNacimiento;
@property (assign, nonatomic) NSInteger dni;
@property (strong, nonatomic) NSString *cuit;

@property (strong, nonatomic) NSString *domicilio;

@end
