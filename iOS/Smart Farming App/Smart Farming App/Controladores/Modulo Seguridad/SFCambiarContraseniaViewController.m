//
//  SFCambiarContraseniaViewController.m
//  Smart Farming App
//
//  Created by Facundo Palma on 10/17/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFCambiarContraseniaViewController.h"

#import "ServiciosModuloSeguridad.h"

@interface SFCambiarContraseniaViewController ()

@end

@implementation SFCambiarContraseniaViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view.
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

-(void)cambiarContrasenia {
    
    NSDictionary *values = [self.form formValues];
    
    SolicitudCambiarContrasenia *solicitud = [SolicitudCambiarContrasenia new];
    
    solicitud.contraseniaActual = [values objectForKey:KEY_CONTRASENIA_VIEJA];
    solicitud.contraseniaNueva = [values objectForKey:KEY_CONTRASENIA_NUEVA];
    
    __weak typeof (self) weakSelf = self;
    
    [self showActivityIndicator];
    [ServiciosModuloSeguridad cambiarContrasenia:solicitud completionBlock:^(RespuestaServicioBase *respuesta) {
        [weakSelf hideActivityIndicator];
        if (respuesta.resultado) {
            [weakSelf userInformationPrompt:kErrorRecuperarCuentaCambioContasenia withCompletion:^{
                [weakSelf.navigationController popViewControllerAnimated:YES];
            }];
        } else {
            [weakSelf handleErrorWithPromptTitle:kErrorCambioContrasenia message:kErrorDesconocido withCompletion:^{
            }];
        }
    } failureBlock:^(ErrorServicioBase *error) {
        [weakSelf hideActivityIndicator];
        [weakSelf handleErrorWithPromptTitle:kErrorCambioContrasenia message:error.detalleError withCompletion:^{
        }];
    }];
}

#pragma mark - Formulario

-(void)initializeForm {
    
    XLFormDescriptor * form;
    XLFormSectionDescriptor * section;
    XLFormRowDescriptor * row;
    
    form = [XLFormDescriptor formDescriptorWithTitle:@"Cambiar contraseña"];
    
    // Seccion contrasenia
    section = [XLFormSectionDescriptor formSectionWithTitle:@"Contraseña"];
    section.footerTitle = @"Su contraseña debe tener al menos 8 caracteres y al menos un número y una letra";
    [form addFormSection:section];
    
    row = [XLFormRowDescriptor formRowDescriptorWithTag:KEY_CONTRASENIA_VIEJA rowType:XLFormRowDescriptorTypePassword title:@"Contraseña actual"];
    [row.cellConfigAtConfigure setObject:@(NSTextAlignmentRight) forKey:@"textField.textAlignment"];
    row.required = YES;
    [section addFormRow:row];
    
    row = [XLFormRowDescriptor formRowDescriptorWithTag:KEY_CONTRASENIA_NUEVA rowType:XLFormRowDescriptorTypePassword title:@"Contraseña nueva"];
    [row.cellConfigAtConfigure setObject:@(NSTextAlignmentRight) forKey:@"textField.textAlignment"];
    row.required = YES;
    [row addValidator:[XLFormRegexValidator formRegexValidatorWithMsg:@"Su contraseña debe tener al menos 8 caracteres y al menos un número y una letra" regex:kRegexContrasenia]];
    [section addFormRow:row];
    
    self.form = form;
}

-(BOOL)validarDatos {
    
    NSArray *formValidationErrors = [self formValidationErrors];
    if ([formValidationErrors count] > 0) {
        for (NSError *error in formValidationErrors) {
            
            XLFormValidationStatus * validationStatus = [[error userInfo] objectForKey:XLValidationStatusErrorKey];
            
            if ([validationStatus.rowDescriptor.tag isEqualToString:KEY_CONTRASENIA_VIEJA]){
                [self markInvalidRowAtIndexPath:[self.form indexPathOfFormRow:validationStatus.rowDescriptor]];
            }
            else if ([validationStatus.rowDescriptor.tag isEqualToString:KEY_CONTRASENIA_NUEVA]){
                [self markInvalidRowAtIndexPath:[self.form indexPathOfFormRow:validationStatus.rowDescriptor]];
            }
        }
        return NO;
    }
    return YES;
}

-(void)hacerLlamadaServicio {
    [self cambiarContrasenia];
}

#pragma mark - Acciones form

- (IBAction)enviarDatos:(UIBarButtonItem *)sender {
    [self enviarForm];
}

@end
