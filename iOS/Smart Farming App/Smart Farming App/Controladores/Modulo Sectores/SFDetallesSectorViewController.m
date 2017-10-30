//
//  SFDetallesSectorViewController.m
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/20/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFDetallesSectorViewController.h"

#import "ServiciosModuloSectores.h"
#import "SFMecanismoRiegoSectorViewController.h"
#import "SFCultivoSectorViewController.h"
#import "SFComponenteSensorSectorViewController.h"

@interface SFDetallesSectorViewController ()

@property (strong, nonatomic) IBOutlet UILabel *nombreLabel;
@property (strong, nonatomic) IBOutlet UILabel *numeroSectorLabel;
@property (strong, nonatomic) IBOutlet UILabel *descripcionLabel;
@property (strong, nonatomic) IBOutlet UILabel *superficieLabel;

@end

@implementation SFDetallesSectorViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view.
}

-(void)viewWillAppear:(BOOL)animated {
    
    self.nombreLabel.text = self.sector.nombreSector;
    self.numeroSectorLabel.text = [NSString stringWithFormat:@"%li@",self.sector.numeroSector];
    self.descripcionLabel.text = self.sector.descripcionSector;
    self.superficieLabel.text = [NSString stringWithFormat:@"%li@", self.sector.superficieSector];
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

#pragma mark - Navigation

// In a storyboard-based application, you will often want to do a little preparation before navigation
- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender {
    // Get the new view controller using [segue destinationViewController].
    // Pass the selected object to the new view controller.
    if ([[segue identifier] isEqualToString:kSFNavegarAInfoCultivoSectorSegue])
    {
        // Get reference to the destination view controller
        SFCultivoSectorViewController *vc = [segue destinationViewController];
        
        // Pass any objects to the view controller here, like...
        vc.idSector = self.sector.idSector;
    } else if ([[segue identifier] isEqualToString:kSFNavegarAInfoMecanismoRiegoSectorSegue])
    {
        // Get reference to the destination view controller
        SFMecanismoRiegoSectorViewController *vc = [segue destinationViewController];
        
        // Pass any objects to the view controller here, like...
        vc.idSector = self.sector.idSector;
    }
    else if ([[segue identifier] isEqualToString:kSFNavegarAInfoComponenteSensorSector])
    {
        // Get reference to the destination view controller
        SFComponenteSensorSectorViewController *vc = [segue destinationViewController];
        
        // Pass any objects to the view controller here, like...
        vc.idSector = self.sector.idSector;
    }
}

@end
