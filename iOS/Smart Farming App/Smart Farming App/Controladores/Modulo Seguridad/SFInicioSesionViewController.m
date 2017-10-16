//
//  SFInicioSesionViewController.m
//  Smart Farming App
//
//  Created by Facundo Palma on 10/11/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFInicioSesionViewController.h"
#import "ServiciosModuloSeguridad.h"

#import "ServiciosModuloFinca.h"

@interface SFInicioSesionViewController ()

@property (strong, nonatomic) IBOutlet UIScrollView *signInScrollView;
@property (weak, nonatomic) IBOutlet UITextField *usuarioTextField;
@property (weak, nonatomic) IBOutlet UITextField *contraseniaTextField;


@end

@implementation SFInicioSesionViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    
    self.viewScrollView = self.signInScrollView;
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

#pragma mark - Accion botones

- (IBAction)iniciarSesionAction:(UIButton *)sender {
    SolicitudInicioSesion *solicitud = [SolicitudInicioSesion new];
    
    __weak typeof(self) weakSelf = self;
    
    solicitud.usuario = self.usuarioTextField.text;
    solicitud.contrasenia = self.contraseniaTextField.text;
    
    [self showActivityIndicator];
    [ServiciosModuloSeguridad iniciarSesion:solicitud completionBlock:^(RespuestaServicioBase *respuesta) {
        [weakSelf hideActivityIndicator];
        
        if (respuesta.resultado) {
            [weakSelf performSegueWithIdentifier:kSFNavegarEstadoAutenticadoSegue sender:self];
        } else {
            [weakSelf handleErrorWithPromptTitle:kErrorInicioSesion message:kErrorDesconocido withCompletion:^{
            }];
        }
        
    } failureBlock:^(ErrorServicioBase *error) {
        [weakSelf hideActivityIndicator];
        [weakSelf handleErrorWithPromptTitle:kErrorInicioSesion message:error.detalleError withCompletion:^{
        }];
    }];
}

#pragma mark - Navigation

// In a storyboard-based application, you will often want to do a little preparation before navigation
- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender {
    // Get the new view controller using [segue destinationViewController].
    // Pass the selected object to the new view controller.
}

@end
