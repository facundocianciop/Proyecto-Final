//
//  PRConstantesComunes.h
//  proyectoRiego2017
//
//  Created by Facundo José Palma on 9/21/17.
//  Copyright © 2017 Facundo José Palma. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface SFConstantesComunes : NSObject

#pragma mark - UIItems

extern NSString *const kSFNavigationBarBackButtonText;
extern NSString *const kSFDefaultPrimaryAction;
extern NSString *const kSFDefaultSecondaryAction;

#pragma mark - Colores

extern NSString *const kColorCeleste;
extern NSString *const kColorCelesteHex;
extern NSString *const kColorVerde;
extern NSString *const kColorVerdeHex;
extern NSString *const kColorVerdeClaro;
extern NSString *const kColorVerdeClaroHex;
extern NSString *const kColorVerdeMasClaro;
extern NSString *const kColorVerdeMasClaroHex;

#pragma mark - Mensajes Roles/Estados

extern NSString *const kRolEncargado;

#pragma mark - Mensajes errores

extern NSString *const kErrorDesconocido;
extern NSString *const kErrorInicioSesion;
extern NSString *const kErrorObteniendoRoles;
extern NSString *const kErrorObteniendoFincas;

@end
