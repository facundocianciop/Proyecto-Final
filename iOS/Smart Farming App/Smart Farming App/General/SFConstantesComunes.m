//
//  PRConstantesComunes.m
//  proyectoRiego2017
//
//  Created by Facundo José Palma on 9/21/17.
//  Copyright © 2017 Facundo José Palma. All rights reserved.
//

#import "SFConstantesComunes.h"

@implementation SFConstantesComunes

#pragma mark - UIItems

NSString *const kSFNavigationBarBackButtonText = @"Volver";
NSString *const kSFDefaultPrimaryAction     = @"Aceptar";
NSString *const kSFDefaultSecondaryAction   = @"Cancelar";

#pragma mark - Colores

NSString *const kColorCeleste = @"Celeste";
NSString *const kColorCelesteHex = @"#41B6E6";
NSString *const kColorVerde = @"Verde";
NSString *const kColorVerdeHex = @"#43B02A";
NSString *const kColorVerdeClaro = @"VerdeClaro";
NSString *const kColorVerdeClaroHex = @"#97D700";
NSString *const kColorVerdeMasClaro = @"VerdeMasClaro";
NSString *const kColorVerdeMasClaroHex = @"#C5E86C";

#pragma mark - Mensajes Roles/Estados

NSString *const kRolEncargado = @"encargado";

#pragma mark - Regex

NSString *const kRegexContrasenia = @"^(?=.*[0-9]+.*)(?=.*[a-zA-Z]+.*)[0-9a-zA-Z]{6,32}$";
NSString *const kRegexDNI = @"(^$|^([0-9]{8}))";
NSString *const kRegexCUIT = @"(^$|^\\d{2}\\-\\d{8}\\-\\d{1}$)";

#pragma mark - Mensajes confirmacion

NSString *const kConfirmacionRegistroUsuario = @"Usuario registrado correctamente";
NSString *const kConfirmacionEnvioMailRecuperacionCuenta = @"Se envió un mail a su cuenta con un código de verificación";
NSString *const kConfirmacionCambioContraseniaRecuperacionCuenta = @"Su nueva contraseña se estableció correctamente";

NSString *const kConfirmacionModificacionUsuario = @"Usuario modificado correctamente";
NSString *const kConfirmacionCambioContrasenia = @"Contraseña modificada";

#pragma mark - Mensajes errores

NSString *const kErrorDesconocido = @"Error desconocido";

NSString *const kErrorRegistroUsuario = @"Error registrando usuario";
NSString *const kErrorRecuperarCuenta = @"Error recuperando cuenta";
NSString *const kErrorRecuperarCuentaCambioContasenia = @"Error estableciendo contraseña nueva";

NSString *const kErrorInicioSesion = @"Error de inicio de sesión";
NSString *const kErrorObteniendoDatosUsuario = @"Error obteniendo datos de usuario";

NSString *const kErrorModificacionUsuario = @"Error modificando usuario";
NSString *const kErrorCambioContrasenia = @"Error cambiando contraseña";

NSString *const kErrorObteniendoRoles = @"Error obteniendo roles";
NSString *const kErrorObteniendoFincas = @"Error obteniendo fincas";

@end
