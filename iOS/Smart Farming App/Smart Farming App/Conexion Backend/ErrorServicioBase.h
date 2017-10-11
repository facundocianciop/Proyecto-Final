//
//  ErrorServicioBase.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/11/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface ErrorServicioBase : NSError

@property (strong, nonatomic) NSString *codigoError;
@property (strong, nonatomic) NSString *detalleError;

@end
