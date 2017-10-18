//
//  IdentificadoresSegue.h
//  Smart Farming App
//
//  Created by Facundo Palma on 10/12/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface IdentificadoresSegue : NSObject

#pragma mark - Modulo Seguridad
extern NSString *const kSFNavegarEstadoAutenticadoSegue;
extern NSString *const kSFNavegarEstadoNoAutenticadoSegue;

extern NSString *const kSFNavegarRecuperarCuentaSegundoPaso;

#pragma mark - Modulo Finca
extern NSString *const kSFNavegarASeccionFincaSegue;

#pragma mark - Modulo Sectores

extern NSString *const kSFNavegarAInfoSectorSegue;

@end
