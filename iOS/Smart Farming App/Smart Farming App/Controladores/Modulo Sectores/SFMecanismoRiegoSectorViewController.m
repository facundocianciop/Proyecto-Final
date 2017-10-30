//
//  SFMecanismoRiegoSectorViewController.m
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/30/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFMecanismoRiegoSectorViewController.h"

#import "ServiciosModuloSectores.h"

#import "SFConfiguracionesRiegoViewController.h"

@interface SFMecanismoRiegoSectorViewController ()

@property (assign, nonatomic) long idMecanismoRiegoSector;

@property (strong, nonatomic) IBOutlet UILabel *nombreLabel;
@property (strong, nonatomic) IBOutlet UILabel *caudalLabel;
@property (strong, nonatomic) IBOutlet UILabel *presionLabel;

@end

@implementation SFMecanismoRiegoSectorViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view.
    
    [self obtenerDatos];
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
     if ([[segue identifier] isEqualToString:kSFNavegarConfiguracionesRiegoSegue])
     {
         // Get reference to the destination view controller
         SFConfiguracionesRiegoViewController *vc = [segue destinationViewController];
         
         // Pass any objects to the view controller here, like...
         vc.idMecanismoRiegoSector = self.idMecanismoRiegoSector;
         vc.idSector = self.idSector;
     }
 }

#pragma mark - Servicio

-(void) obtenerDatos {
    __weak typeof(self) weakSelf = self;
    
    SolicitudMostrarMecanismoRiegoSector *solicitud = [SolicitudMostrarMecanismoRiegoSector new];
    solicitud.idFinca = [[ContextoUsuario instance] fincaSeleccionada];
    solicitud.idSector = self.idSector;
    
    [ServiciosModuloSectores mostrarMecanismoRiegoSector:solicitud completionBlock:^(RespuestaServicioBase *respuesta) {
        [weakSelf hideActivityIndicator];
        
        if ([respuesta isKindOfClass:[RespuestaMostrarMecanismoRiegoSector class]]) {
            RespuestaMostrarMecanismoRiegoSector *respuestaMostrarMecanismoRiegoSector = (RespuestaMostrarMecanismoRiegoSector *)respuesta;
            
            if (respuestaMostrarMecanismoRiegoSector.resultado) {
                
                self.nombreLabel.text = respuestaMostrarMecanismoRiegoSector.mecanismoRiegoFincaSector.nombreTipoMecanismo;
                self.caudalLabel.text = [NSString stringWithFormat:@"%f", respuestaMostrarMecanismoRiegoSector.mecanismoRiegoFincaSector.caudal];
                self.presionLabel.text = [NSString stringWithFormat:@"%f", respuestaMostrarMecanismoRiegoSector.mecanismoRiegoFincaSector.presion];
                
                self.idMecanismoRiegoSector = respuestaMostrarMecanismoRiegoSector.mecanismoRiegoFincaSector.idMecanismoRiegoFincaSector;
                
            } else {
                [weakSelf handleErrorWithPromptTitle:@"Error obteniendo mecanismo" message:kErrorDesconocido withCompletion:^{
                }];
            }
        }
    } failureBlock:^(ErrorServicioBase *error) {
        [weakSelf hideActivityIndicator];
        [weakSelf handleErrorWithPromptTitle:@"Error obteniendo mecanismo" message:error.detalleError withCompletion:^{
        }];
    }];
}

@end
