//
//  BaseServicios.h
//  proyectoRIego2017
//
//  Created by Facundo José Palma on 9/21/17.
//  Copyright © 2017 Facundo José Palma. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "HTTPConector.h"

#pragma mark - Keys Diccionarios

#define PARAM_USER_ID           @"nro_usuario"
#define PARAM_CLIENT_ID         @"nro_cliente"

// LOGIN

#define PARAM_USERNAME          @"login_usuario"
#define PARAM_PASSWORD          @"login_password"

// LOGOUT

#define PARAM_SESSION_ID        @"nro_sesion"


@interface BaseServicios : NSObject

@end
