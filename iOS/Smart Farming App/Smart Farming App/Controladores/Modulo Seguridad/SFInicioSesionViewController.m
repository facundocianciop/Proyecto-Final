//
//  SFInicioSesionViewController.m
//  Smart Farming App
//
//  Created by Facundo Palma on 10/11/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFInicioSesionViewController.h"
#import "ServiciosModuloSeguridad.h"

@interface SFInicioSesionViewController ()

@property (weak, nonatomic) IBOutlet UITextField *usuarioTextField;
@property (weak, nonatomic) IBOutlet UITextField *contraseniaTextField;


@end

@implementation SFInicioSesionViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view.
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
        [self hideActivityIndicator];
        
        [weakSelf performSegueWithIdentifier:kSFNavegarEstadoAutenticadoSegue sender:self];
        
    } failureBlock:^(ErrorServicioBase *error) {
        [self hideActivityIndicator];
        
        
    }];
}

#pragma mark - Navigation

// In a storyboard-based application, you will often want to do a little preparation before navigation
- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender {
    // Get the new view controller using [segue destinationViewController].
    // Pass the selected object to the new view controller.
}

@end
