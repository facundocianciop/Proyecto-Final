//
//  SFPerfilUsuarioViewController.m
//  Smart Farming App
//
//  Created by Facundo Palma on 10/16/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFPerfilUsuarioViewController.h"

#import "ServiciosModuloSeguridad.h"
#import "ContextoUsuario.h"

#import "SFModificarUsuarioViewController.h"

@interface SFPerfilUsuarioViewController ()

@property (weak, nonatomic) IBOutlet UIImageView *imagenUsuario;

@property (weak, nonatomic) IBOutlet UILabel *username;
@property (weak, nonatomic) IBOutlet UILabel *email;
@property (weak, nonatomic) IBOutlet UILabel *nombre;

@property (weak, nonatomic) IBOutlet UILabel *fechaNacimiento;
@property (weak, nonatomic) IBOutlet UILabel *dni;
@property (weak, nonatomic) IBOutlet UILabel *cuit;
@property (weak, nonatomic) IBOutlet UILabel *domicilio;

@property (strong, nonatomic) NSString *emailData;
@property (strong, nonatomic) NSString *nombreData;
@property (strong, nonatomic) NSString *apellidoData;
@property (strong, nonatomic) NSDate *fechaNacimientoData;
@property (assign, nonatomic) NSInteger dniData;
@property (strong, nonatomic) NSString *cuitData;
@property (strong, nonatomic) NSString *domicilioData;

@end

@implementation SFPerfilUsuarioViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view.
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

-(void)viewWillAppear:(BOOL)animated {
    [super viewWillAppear:animated];
    
    [self obtenerDatosUsuario];
}
#pragma mark - Navigation

// In a storyboard-based application, you will often want to do a little preparation before navigation
- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender {
    if ([[segue identifier] isEqualToString:kSFNavegarModificarUsuarioSegue]) {
        SFModificarUsuarioViewController *vc = [segue destinationViewController];
        vc.emailRow.value = self.emailData;
        vc.nombreRow.value = self.nombreData;
        vc.apellidoRow.value = self.apellidoData;
        vc.fechaNacimientoRow.value = self.fechaNacimientoData;
        if (self.dniData == 0) {
            vc.dniRow.value = @"";
        } else {
            vc.dniRow.value = [NSString stringWithFormat:@"%li", self.dniData];
        }
        vc.cuitRow.value = self.cuitData;
        vc.domicilioRow.value = self.domicilioData;
    }
}

#pragma mark - private

-(void)cerrarSesion {
    [[ContextoUsuario instance] invalidateContext];
    [self.navigationController popToRootViewControllerAnimated:YES];
}

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

-(void)llamadaCerrarSesion {

    __weak typeof (self) weakSelf = self;
    
    [self showActivityIndicator];
    [ServiciosModuloSeguridad finalizarSesion:^(RespuestaServicioBase *respuesta) {
        [weakSelf hideActivityIndicator];
        [self cerrarSesion];
    } failureBlock:^(ErrorServicioBase *error) {
        [weakSelf hideActivityIndicator];
        [self cerrarSesion];
    }];
}

#pragma mark - Configurar UI

-(void)setInformacionUsuario:(RespuestaMostrarUsuario*)datosUsuario {
    
    self.username.text = datosUsuario.username;
    self.email.text = datosUsuario.email;
    self.emailData = datosUsuario.email;
    
    self.nombre.text = [NSString stringWithFormat:@"%@ %@", datosUsuario.nombre, datosUsuario.apellido];
    self.nombreData = datosUsuario.username;
    self.apellidoData = datosUsuario.apellido;
    
    if (datosUsuario.fechaNacimiento) {
        self.fechaNacimiento.text = [SFUtils formatDateDDMMYYYY: datosUsuario.fechaNacimiento];
        self.fechaNacimientoData = datosUsuario.fechaNacimiento;
    }
    if (datosUsuario.dni) {
        self.dni.text = [NSString stringWithFormat:@"%li", datosUsuario.dni];
        self.dniData = datosUsuario.dni;
    }
    if (datosUsuario.cuit) {
        self.cuit.text = datosUsuario.cuit;
        self.cuitData = datosUsuario.cuit;
    }
    if (datosUsuario.domicilio) {
        self.domicilio.text = datosUsuario.domicilio;
        self.domicilioData = datosUsuario.domicilio;
    }
}

#pragma mark - Acciones

- (IBAction)cerrarSesion:(id)sender {
    [self llamadaCerrarSesion];
}

@end
