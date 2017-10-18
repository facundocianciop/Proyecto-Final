//
//  SFPerfilUsuarioViewController.m
//  Smart Farming App
//
//  Created by Facundo Palma on 10/16/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFPerfilUsuarioViewController.h"

#import "ServiciosModuloSeguridad.h"
#import "AppDelegate.h"

@interface SFPerfilUsuarioViewController ()

@property (weak, nonatomic) IBOutlet UIImageView *imagenUsuario;

@property (weak, nonatomic) IBOutlet UILabel *username;
@property (weak, nonatomic) IBOutlet UILabel *email;
@property (weak, nonatomic) IBOutlet UILabel *nombre;

@property (weak, nonatomic) IBOutlet UILabel *fechaNacimiento;
@property (weak, nonatomic) IBOutlet UILabel *dni;
@property (weak, nonatomic) IBOutlet UILabel *cuit;
@property (weak, nonatomic) IBOutlet UILabel *domicilio;

@end

@implementation SFPerfilUsuarioViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view.
    
    [self obtenerDatosUsuario];
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

#pragma mark - Llamadas servicio

-(void)obtenerDatosUsuario {
    __weak typeof(self) weakSelf = self;
    
    [self showActivityIndicator];
    [ServiciosModuloSeguridad mostrarUsuario:^(RespuestaServicioBase *respuesta) {
        [weakSelf hideActivityIndicator];
        
        if ([respuesta isKindOfClass:[RespuestaMostrarUsuario class]] && respuesta.resultado) {
            
            RespuestaMostrarUsuario *respuestaMostrarUsuario = (RespuestaMostrarUsuario*)respuesta;
            
            [weakSelf setInformacionUsuario:respuestaMostrarUsuario];
            
        } else {
            [weakSelf handleErrorWithPromptTitle:kErrorObteniendoDatosUsuario message:kErrorDesconocido withCompletion:^{
            }];
        }
        
    } failureBlock:^(ErrorServicioBase *error) {
        [weakSelf hideActivityIndicator];
        [weakSelf handleErrorWithPromptTitle:kErrorObteniendoDatosUsuario message:error.detalleError withCompletion:^{
        }];
    }];
}

-(void)cerrarSesion {

    __weak typeof (self) weakSelf = self;
    
    [self showActivityIndicator];
    [ServiciosModuloSeguridad finalizarSesion:^(RespuestaServicioBase *respuesta) {
        [weakSelf hideActivityIndicator];
        
        AppDelegate *appDelegate = (AppDelegate*) [[UIApplication sharedApplication]delegate];
        [appDelegate forzarCierreSesion];
        
    } failureBlock:^(ErrorServicioBase *error) {
        [weakSelf hideActivityIndicator];
        
        AppDelegate *appDelegate = (AppDelegate*) [[UIApplication sharedApplication]delegate];
        [appDelegate forzarCierreSesion];
        
    }];
}

#pragma mark - Configurar UI

-(void)setInformacionUsuario:(RespuestaMostrarUsuario*)datosUsuario {
    
    self.username.text = datosUsuario.username;
    self.email.text = datosUsuario.email;
    
    self.nombre.text = [NSString stringWithFormat:@"%@ %@", datosUsuario.username, datosUsuario.apellido];
    
    self.fechaNacimiento.text = [SFUtils formatDateDDMMYYYY: datosUsuario.fechaNacimiento];
    self.dni.text = [NSString stringWithFormat:@"%li", datosUsuario.dni];
    self.cuit.text = datosUsuario.cuit;
    self.domicilio.text = datosUsuario.domicilio;
}

#pragma mark - Acciones

- (IBAction)cerrarSesion:(id)sender {
    
    [self cerrarSesion];
}

@end
