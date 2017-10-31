//
//  SFReporteEventosPersonalizadosRegistradosViewController.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/31/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFTableViewControllerBase.h"

#import "SFConfiguracionEvento.h"
#import "SFSectorFinca.h"

@interface SFReporteEventosPersonalizadosRegistradosViewController : SFTableViewControllerBase

@property (strong, nonatomic) SFSectorFinca *sector;
@property (strong, nonatomic) SFConfiguracionEvento *configuracionEvento;

@end
