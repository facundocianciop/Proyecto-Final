//
//  SFCultivoSectorViewController.m
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/30/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFCultivoSectorViewController.h"

#import "ServiciosModuloSectores.h"

@interface SFCultivoSectorViewController ()

@property (strong, nonatomic) IBOutlet UILabel *nombreLabel;
@property (strong, nonatomic) IBOutlet UILabel *descripcionLabel;
@property (strong, nonatomic) IBOutlet UILabel *tipoCultivoLabel;
@property (strong, nonatomic) IBOutlet UILabel *subTipoCultivoLabel;
@property (strong, nonatomic) IBOutlet UILabel *fechaPlantacionLabel;

@end

@implementation SFCultivoSectorViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view.
    
    [self obtenerDatos];
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

/*
#pragma mark - Navigation

// In a storyboard-based application, you will often want to do a little preparation before navigation
- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender {
    // Get the new view controller using [segue destinationViewController].
    // Pass the selected object to the new view controller.
}
*/

#pragma mark - Servicio

-(void) obtenerDatos {
    __weak typeof(self) weakSelf = self;
    
    SolicitudMostrarCultivoSector *solicitud = [SolicitudMostrarCultivoSector new];
    solicitud.idFinca = [[ContextoUsuario instance] fincaSeleccionada];
    solicitud.idSector = self.idSector;
    
    [ServiciosModuloSectores mostrarCultivoSector:solicitud completionBlock:^(RespuestaServicioBase *respuesta) {
        
        [weakSelf hideActivityIndicator];
        
        if ([respuesta isKindOfClass:[RespuestaMostrarCultivoSector class]]) {
            RespuestaMostrarCultivoSector *respuestaMostrarCultivoSector = (RespuestaMostrarCultivoSector *)respuesta;
            
            if (respuestaMostrarCultivoSector.resultado) {
                
                self.nombreLabel.text = respuestaMostrarCultivoSector.cultivoSector.nombreCultivoSector;
                self.descripcionLabel.text = respuestaMostrarCultivoSector.cultivoSector.descripcionCultivoSector;
                self.tipoCultivoLabel.text = respuestaMostrarCultivoSector.cultivoSector.tipoCultivo;
                self.subTipoCultivoLabel.text = respuestaMostrarCultivoSector.cultivoSector.subTipoCultivo;
                self.fechaPlantacionLabel.text = [SFUtils formatDateDDMMYYYY:respuestaMostrarCultivoSector.cultivoSector.fechaPlantacionCultivoSector];
            } else {
                [weakSelf handleErrorWithPromptTitle:@"Error obteniendo cultivo" message:kErrorDesconocido withCompletion:^{
                }];
            }
        }
    } failureBlock:^(ErrorServicioBase *error) {
        [weakSelf hideActivityIndicator];
        [weakSelf handleErrorWithPromptTitle:@"Error obteniendo cultivo" message:error.detalleError withCompletion:^{
        }];
    }];
}

@end
