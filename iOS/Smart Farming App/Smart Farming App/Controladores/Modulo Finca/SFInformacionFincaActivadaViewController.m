//
//  SFInformacionFincaActivadaViewController.m
//  Smart Farming App
//
//  Created by Facundo Palma on 10/15/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFInformacionFincaActivadaViewController.h"

#import "ServiciosModuloFinca.h"

@interface SFInformacionFincaActivadaViewController ()

@property (strong, nonatomic) IBOutlet UILabel *nombreFincaLabel;
@property (strong, nonatomic) IBOutlet UILabel *rolUsuarioLabel;
@property (strong, nonatomic) IBOutlet UILabel *ubicacionFincaLabel;
@property (strong, nonatomic) IBOutlet UILabel *direccionLegalLabel;
@property (strong, nonatomic) IBOutlet UILabel *tamanioFincaLabel;

@end

@implementation SFInformacionFincaActivadaViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view.
    
    [self obtenerDatosFinca];
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

#pragma mark - Privado

-(void) obtenerDatosFinca {
    
    SolicitudBuscarFincaId *solitud = [SolicitudBuscarFincaId new];
    solitud.idFinca = [[ContextoUsuario instance] fincaSeleccionada];
    
    __weak typeof (self)weakSelf = self;
    
    [self showActivityIndicator];
    [ServiciosModuloFinca buscarFincaId:solitud completionBlock:^(RespuestaServicioBase *respuesta) {
        [weakSelf hideActivityIndicator];
        
        if ([respuesta isKindOfClass:[RespuestaBuscarFincaId class]]) {
            RespuestaBuscarFincaId *respuestaBuscarFincaId = (RespuestaBuscarFincaId *)respuesta;
            
            if (respuestaBuscarFincaId.resultado) {
                
                self.nombreFincaLabel.text = respuestaBuscarFincaId.finca.nombre;
                self.rolUsuarioLabel.text = respuestaBuscarFincaId.finca.rolUsuario;
                self.ubicacionFincaLabel.text = respuestaBuscarFincaId.finca.ubicacion;
                self.direccionLegalLabel.text = respuestaBuscarFincaId.finca.direccionLegal;
                self.tamanioFincaLabel.text = [NSString stringWithFormat:@"%li",respuestaBuscarFincaId.finca.tamanio];
                
            } else {
                [weakSelf handleErrorWithPromptTitle:kErrorObteniendoDatosFinca message:kErrorDesconocido withCompletion:^{
                    [self.navigationController popViewControllerAnimated:YES];
                }];
            }
        }
    } failureBlock:^(ErrorServicioBase *error) {
        [weakSelf hideActivityIndicator];
        [weakSelf handleErrorWithPromptTitle:kErrorObteniendoDatosFinca message:error.detalleError withCompletion:^{
            [self.navigationController popViewControllerAnimated:YES];
        }];
    }];
}

#pragma mark - Acciones

- (IBAction)accionVolver:(UIBarButtonItem *)sender {
}


@end
