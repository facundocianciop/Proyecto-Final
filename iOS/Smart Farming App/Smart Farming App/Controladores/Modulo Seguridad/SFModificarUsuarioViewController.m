//
//  SFModificarUsuarioViewController.m
//  Smart Farming App
//
//  Created by Facundo Palma on 10/17/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFModificarUsuarioViewController.h"

#import "ServiciosModuloSeguridad.h"

@interface SFModificarUsuarioViewController ()

@end

@implementation SFModificarUsuarioViewController

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

-(void)modificarUsuario {
    NSDictionary *values = [self.form formValues];
    
    SolicitudModificarUsuario *solicitud = [SolicitudModificarUsuario new];
    
    solicitud.email = [values objectForKey:KEY_EMAIL];
    
    solicitud.nombre = [values objectForKey:KEY_NOMBRE_USUARIO];
    solicitud.apellido = [values objectForKey:KEY_APELLIDO_USUARIO];
   
    if ([values objectForKey:KEY_FECHA_NACIMIENTO] != [NSNull null]) {
        solicitud.fechaNacimiento = [values objectForKey:KEY_FECHA_NACIMIENTO];
    }
    if ([values objectForKey:KEY_DNI] != [NSNull null]) {
        solicitud.dni = [[values objectForKey:KEY_DNI] integerValue];
    }
    if ([values objectForKey:KEY_CUIT] != [NSNull null]) {
        solicitud.cuit = [values objectForKey:KEY_CUIT];
    }
    if ([values objectForKey:KEY_DOMICILIO] != [NSNull null]) {
        solicitud.domicilio = [values objectForKey:KEY_DOMICILIO];
    }
    
    __weak typeof (self) weakSelf = self;
    
    [self showActivityIndicator];
    [ServiciosModuloSeguridad modificarUsuario:solicitud completionBlock:^(RespuestaServicioBase *respuesta) {
        [weakSelf hideActivityIndicator];
        if (respuesta.resultado) {
            [weakSelf userInformationPrompt:kConfirmacionModificacionUsuario withCompletion:^{
                [weakSelf.navigationController popViewControllerAnimated:YES];
            }];
        } else {
            [weakSelf handleErrorWithPromptTitle:kErrorModificacionUsuario message:kErrorDesconocido withCompletion:^{
            }];
        }
    } failureBlock:^(ErrorServicioBase *error) {
        [weakSelf hideActivityIndicator];
        [weakSelf handleErrorWithPromptTitle:kErrorModificacionUsuario message:error.detalleError withCompletion:^{
        }];
    }];
}

#pragma mark - Formulario

-(void)initializeForm {
    
    XLFormDescriptor * form;
    XLFormSectionDescriptor * section;
    
    form = [XLFormDescriptor formDescriptorWithTitle:@"Modificar usuario"];
    
    // Seccion informacion obligatoria
    section = [XLFormSectionDescriptor formSectionWithTitle:@"Usuario"];
    [form addFormSection:section];
    
    self.emailRow = [XLFormRowDescriptor formRowDescriptorWithTag:KEY_EMAIL rowType:XLFormRowDescriptorTypeEmail title:@"Email"];
    [self.emailRow.cellConfigAtConfigure setObject:@"Email" forKey:@"textField.placeholder"];
    [self.emailRow.cellConfigAtConfigure setObject:@(NSTextAlignmentRight) forKey:@"textField.textAlignment"];
    self.emailRow.required = YES;
    [self.emailRow addValidator:[XLFormValidator emailValidator]];
    [section addFormRow:self.emailRow];
    
    self.nombreRow = [XLFormRowDescriptor formRowDescriptorWithTag:KEY_NOMBRE_USUARIO rowType:XLFormRowDescriptorTypeName title:@"Nombre"];
    [self.nombreRow.cellConfigAtConfigure setObject:@"Nombre" forKey:@"textField.placeholder"];
    [self.nombreRow.cellConfigAtConfigure setObject:@(NSTextAlignmentRight) forKey:@"textField.textAlignment"];
    self.nombreRow.required = YES;
    [section addFormRow:self.nombreRow];
    
    self.apellidoRow = [XLFormRowDescriptor formRowDescriptorWithTag:KEY_APELLIDO_USUARIO rowType:XLFormRowDescriptorTypeName title:@"Apellido"];
    [self.apellidoRow.cellConfigAtConfigure setObject:@"Apellido" forKey:@"textField.placeholder"];
    [self.apellidoRow.cellConfigAtConfigure setObject:@(NSTextAlignmentRight) forKey:@"textField.textAlignment"];
    self.apellidoRow.required = YES;
    [section addFormRow:self.apellidoRow];
    
    // Seccion informacion opcional
    section = [XLFormSectionDescriptor formSectionWithTitle:@"Datos adicionales"];
    [form addFormSection:section];
    
    self.fechaNacimientoRow = [XLFormRowDescriptor formRowDescriptorWithTag:KEY_FECHA_NACIMIENTO rowType:XLFormRowDescriptorTypeDate title:@"Fecha de Nacimiento"];
    [section addFormRow:self.fechaNacimientoRow];
    
    self.dniRow = [XLFormRowDescriptor formRowDescriptorWithTag:KEY_DNI rowType:XLFormRowDescriptorTypeNumber title:@"D.N.I."];
    [self.dniRow.cellConfigAtConfigure setObject:@"D.N.I." forKey:@"textField.placeholder"];
    [self.dniRow.cellConfigAtConfigure setObject:@(NSTextAlignmentRight) forKey:@"textField.textAlignment"];
    [self.dniRow addValidator:[XLFormRegexValidator formRegexValidatorWithMsg:@"Ingresar solo numeros" regex:kRegexDNI]];
    [self.dniRow.cellConfigAtConfigure setObject:@(8) forKey:@"textFieldMaxNumberOfCharacters"];
    [section addFormRow:self.dniRow];
    
    self.cuitRow = [XLFormRowDescriptor formRowDescriptorWithTag:KEY_CUIT rowType:XLFormRowDescriptorTypeText title:@"C.U.I.T."];
    [self.cuitRow.cellConfigAtConfigure setObject:@"C.U.I.T." forKey:@"textField.placeholder"];
    [self.cuitRow.cellConfigAtConfigure setObject:@(NSTextAlignmentRight) forKey:@"textField.textAlignment"];
    [self.cuitRow addValidator:[XLFormRegexValidator formRegexValidatorWithMsg:@"C.U.I.T debe llevar guiones" regex:kRegexCUIT]];
    [self.cuitRow.cellConfigAtConfigure setObject:@(13) forKey:@"textFieldMaxNumberOfCharacters"];
    [section addFormRow:self.cuitRow];
    
    self.domicilioRow = [XLFormRowDescriptor formRowDescriptorWithTag:KEY_DOMICILIO rowType:XLFormRowDescriptorTypeText title:@"Domicilio"];
    [self.domicilioRow.cellConfigAtConfigure setObject:@"Domicilio" forKey:@"textField.placeholder"];
    [self.domicilioRow.cellConfigAtConfigure setObject:@(NSTextAlignmentRight) forKey:@"textField.textAlignment"];
    [self.domicilioRow.cellConfigAtConfigure setObject:@(50) forKey:@"textFieldMaxNumberOfCharacters"];
    [section addFormRow:self.domicilioRow];
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
            else if ([validationStatus.rowDescriptor.tag isEqualToString:KEY_NOMBRE_USUARIO]){
                [self markInvalidRowAtIndexPath:[self.form indexPathOfFormRow:validationStatus.rowDescriptor]];
            }
            else if ([validationStatus.rowDescriptor.tag isEqualToString:KEY_APELLIDO_USUARIO]){
                [self markInvalidRowAtIndexPath:[self.form indexPathOfFormRow:validationStatus.rowDescriptor]];
            }
            else if ([validationStatus.rowDescriptor.tag isEqualToString:KEY_DNI]){
                [self markInvalidRowAtIndexPath:[self.form indexPathOfFormRow:validationStatus.rowDescriptor]];
            }
            else if ([validationStatus.rowDescriptor.tag isEqualToString:KEY_CUIT]){
                [self markInvalidRowAtIndexPath:[self.form indexPathOfFormRow:validationStatus.rowDescriptor]];
            }
        }
        return NO;
    }
    return YES;
}

-(void)hacerLlamadaServicio {
    [self modificarUsuario];
}

#pragma mark - Acciones form

- (IBAction)enviarDatos:(UIBarButtonItem *)sender {
    [self enviarForm];
}

@end
