//
//  SFDatosFincaHelper.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/27/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <Foundation/Foundation.h>

typedef void(^resultadoBlock)(BOOL *resultado);

@interface SFDatosFincaHelper : NSObject

+(void)obtenerDatosFinca:(long)idFinca withCompletion:(resultadoBlock*)resultado;

@end
