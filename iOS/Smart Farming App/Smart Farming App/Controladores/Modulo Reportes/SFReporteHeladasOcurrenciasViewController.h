//
//  SFReporteHeladasOcurrenciasViewController.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/31/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFTableViewControllerBase.h"

@interface SFReporteHeladasOcurrenciasViewController : SFTableViewControllerBase

@property (assign, nonatomic) long idSector;

@property (strong, nonatomic) NSDate *fechaInicioSector;
@property (strong, nonatomic) NSDate *fechaFinSector;

@end
