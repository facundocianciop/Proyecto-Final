//
//  SFRecuperarCuentaViewController.m
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/12/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFRecuperarCuentaViewController.h"

#import "ServiciosModuloSeguridad.h"
#import "SFRecuperarCuentaNuevaContraseniaViewController.h"

@interface SFRecuperarCuentaViewController ()

@property (strong, nonatomic) NSString *username;

@end

@implementation SFRecuperarCuentaViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view.
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

#pragma mark - Navigation

// In a storyboard-based application, you will often want to do a little preparation before navigation
- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender {
    if ([[segue identifier] isEqualToString:kSFNavegarRecuperarCuentaSegundoPaso]) {
        SFRecuperarCuentaNuevaContraseniaViewController *vc = [segue destinationViewController];
        vc.username = self.username;
    }
}

#pragma mark - Llamadas servicio

-(void)recuperarCuenta {
    
    NSDictionary *values = [self.form formValues];

    SolicitudRecuperarCuenta *solicitud = [SolicitudRecuperarCuenta new];
    
    solicitud.email = [values objectForKey:KEY_EMAIL];
    
    __weak typeof (self) weakSelf = self;
    
    [self showActivityIndicator];
    [ServiciosModuloSeguridad recuperarCuenta:solicitud completionBlock:^(RespuestaServicioBase *respuesta) {
        [weakSelf hideActivityIndicator];
        if (respuesta.resultado) {
            if ([respuesta isKindOfClass:[RespuestaRecuperarCuenta class]]) {
                RespuestaRecuperarCuenta *respuestaRecuperarCuenta = (RespuestaRecuperarCuenta *)respuesta;
                weakSelf.username = respuestaRecuperarCuenta.username;
                [weakSelf userInformationPrompt:kConfirmacionEnvioMailRecuperacionCuenta withCompletion:^{
                    [weakSelf performSegueWithIdentifier:kSFNavegarRecuperarCuentaSegundoPaso sender:self];
                }];
            }
        } else {
            [weakSelf handleErrorWithPromptTitle:kErrorRecuperarCuenta message:kErrorDesconocido withCompletion:^{
            }];
        }
    } failureBlock:^(ErrorServicioBase *error) {
        [weakSelf hideActivityIndicator];
        [weakSelf handleErrorWithPromptTitle:kErrorRecuperarCuenta message:error.detalleError withCompletion:^{
        }];
    }];
}

#pragma mark - Formulario

-(void)initializeForm {
    
    XLFormDescriptor * form;
    XLFormSectionDescriptor * section;
    XLFormRowDescriptor * row;
    
    form = [XLFormDescriptor formDescriptorWithTitle:@"Recuperar cuenta"];
    
    // Seccion informacion obligatoria
    section = [XLFormSectionDescriptor formSectionWithTitle:@"Ingresar e-mail para recuperar cuenta"];
    [form addFormSection:section];
    
    row = [XLFormRowDescriptor formRowDescriptorWithTag:KEY_EMAIL rowType:XLFormRowDescriptorTypeEmail title:@"Email"];
    [row.cellConfigAtConfigure setObject:@"Email" forKey:@"textField.placeholder"];
    [row.cellConfigAtConfigure setObject:@(NSTextAlignmentRight) forKey:@"textField.textAlignment"];
    row.required = YES;
    [row addValidator:[XLFormValidator emailValidator]];
    [section addFormRow:row];
    
    self.form = form;
}

-(BOOL)validarDatos {
    
    NSArray *formValidationErrors = [self formValidationErrors];
    if ([formValidationErrors count] > 0) {
        for (NSError *error in formValidationErrors) {
            
            XLFormValidationStatus * validationStatus = [[error userInfo] objectForKey:XLValidationStatusErrorKey];
            
            if ([validationStatus.rowDescriptor.tag isEqualToString:KEY_EMAIL]){
                [self markInvalidRowAtIndexPath:[self.form indexPathOfFormRow:validationStatus.rowDescriptor]];
            }
        }
        return NO;
    }
    return YES;
}

-(void)hacerLlamadaServicio {
    [self recuperarCuenta];
}

#pragma mark - Acciones form

- (IBAction)enviarDatos:(id)sender {
    [self enviarForm];
}

@end
