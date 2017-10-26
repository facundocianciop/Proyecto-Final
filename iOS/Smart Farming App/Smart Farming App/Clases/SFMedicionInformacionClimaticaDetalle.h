//
//  SFMedicionInformacionClimaticaDetalle.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/25/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <UIKit/UIKit.h>



@interface SFMedicionInformacionClimaticaDetalle : NSObject

@property (assign, nonatomic) NSInteger nroRenglon; // nroRenglon
@property (assign, nonatomic) CGFloat valorMedicion; // valor

@property (strong, nonatomic) NSString *nombreTipoMedicion; // tipoMedicionClimatica

@end
