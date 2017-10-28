//
//  ContextoUsuario.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 9/21/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <Foundation/Foundation.h>

#import "SFConjuntoPermisos.h"

@interface ContextoUsuario : NSObject

#pragma mark - Initialization

+(instancetype)instance;
+(instancetype)instanceWithUsername:(NSString *)username;

#pragma mark - Public

-(NSString *)usuarioActual;

-(void)seleccionarFinca:(long)fincaId;
-(long)fincaSeleccionada;

-(void)setPermisosFincaSeleccionada:(SFConjuntoPermisos*)conjuntoPermisos;
-(SFConjuntoPermisos*)permisosFincaSeleccionada;

-(void)invalidateContext;

@end
