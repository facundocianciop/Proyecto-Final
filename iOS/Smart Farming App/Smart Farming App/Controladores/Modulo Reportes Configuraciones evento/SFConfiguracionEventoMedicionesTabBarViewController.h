//
//  SFConfiguracionEventoMedicionesTabBarViewController.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/30/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <UIKit/UIKit.h>

#import "SFMedicionFuenteInterna.h"
#import "SFMedicionFuenteExterna.h"

@interface SFConfiguracionEventoMedicionesTabBarViewController : UITabBarController

@property (strong, nonatomic) NSArray<SFMedicionFuenteInterna*> *listaMedicionesInternas;
@property (strong, nonatomic) NSArray<SFMedicionFuenteExterna*> *listaMedicionesExternas;

@end
