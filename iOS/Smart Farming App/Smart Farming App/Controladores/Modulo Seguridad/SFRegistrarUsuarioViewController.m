//
//  SFRegistrarUsuarioViewController.m
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/12/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFRegistrarUsuarioViewController.h"

#import "ServiciosModuloSeguridad.h"

@interface SFRegistrarUsuarioViewController ()

@end

@implementation SFRegistrarUsuarioViewController

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

-(void)registrarUsuario {
    
    NSDictionary *values = [self.form formValues];
    
    SolicitudRegistrarUsuario *solicitud = [SolicitudRegistrarUsuario new];
    
    solicitud.usuario = [values objectForKey:KEY_USUARIO];
    solicitud.email = [values objectForKey:KEY_EMAIL];
    solicitud.contrasenia = [values objectForKey:KEY_CONTRASENIA];
    
    solicitud.nombre = [values objectForKey:KEY_NOMBRE_USUARIO];
    solicitud.apellido = [values objectForKey:KEY_APELLIDO_USUARIO];
    solicitud.fechaNacimiento = [values objectForKey:KEY_FECHA_NACIMIENTO];
    if ([values objectForKey:KEY_DNI] != [NSNull null]) {
        solicitud.dni = [[values objectForKey:KEY_DNI] integerValue];
    }
    solicitud.cuit = [values objectForKey:KEY_CUIT];
    solicitud.domicilio = [values objectForKey:KEY_DOMICILIO];
    
    __weak typeof (self) weakSelf = self;
    
    [self showActivityIndicator];
    [ServiciosModuloSeguridad registrarUsuario:solicitud completionBlock:^(RespuestaServicioBase *respuesta) {
        [weakSelf hideActivityIndicator];
        if (respuesta.resultado) {
            [weakSelf userInformationPrompt:kConfirmacionRegistroUsuario withCompletion:^{
                [weakSelf.navigationController popToRootViewControllerAnimated:YES];
            }];
        } else {
            [weakSelf handleErrorWithPromptTitle:kErrorRegistroUsuario message:kErrorDesconocido withCompletion:^{
            }];
        }
    } failureBlock:^(ErrorServicioBase *error) {
        [weakSelf hideActivityIndicator];
        [weakSelf handleErrorWithPromptTitle:kErrorRegistroUsuario message:error.detalleError withCompletion:^{
        }];
    }];
    
}

#pragma mark - Formulario

-(void)initializeForm {
    
    XLFormDescriptor * form;
    XLFormSectionDescriptor * section;
    XLFormRowDescriptor * row;
    
    form = [XLFormDescriptor formDescriptorWithTitle:@"Registrar usuario"];
    
    // Seccion informacion obligatoria
    section = [XLFormSectionDescriptor formSectionWithTitle:@"Usuario"];
    [form addFormSection:section];
    
    row = [XLFormRowDescriptor formRowDescriptorWithTag:KEY_USUARIO rowType:XLFormRowDescriptorTypeAccount title:@"Usuario"];
    [row.cellConfigAtConfigure setObject:@"Usuario" forKey:@"textField.placeholder"];
    [row.cellConfigAtConfigure setObject:@(NSTextAlignmentRight) forKey:@"textField.textAlignment"];
    row.required = YES;
    [section addFormRow:row];
    
    row = [XLFormRowDescriptor formRowDescriptorWithTag:KEY_EMAIL rowType:XLFormRowDescriptorTypeEmail title:@"Email"];
    [row.cellConfigAtConfigure setObject:@"Email" forKey:@"textField.placeholder"];
    [row.cellConfigAtConfigure setObject:@(NSTextAlignmentRight) forKey:@"textField.textAlignment"];
    row.required = YES;
    [row addValidator:[XLFormValidator emailValidator]];
    [section addFormRow:row];
    
    row = [XLFormRowDescriptor formRowDescriptorWithTag:KEY_NOMBRE_USUARIO rowType:XLFormRowDescriptorTypeName title:@"Nombre"];
    [row.cellConfigAtConfigure setObject:@"Nombre" forKey:@"textField.placeholder"];
    [row.cellConfigAtConfigure setObject:@(NSTextAlignmentRight) forKey:@"textField.textAlignment"];
    row.required = YES;
    [section addFormRow:row];
    
    row = [XLFormRowDescriptor formRowDescriptorWithTag:KEY_APELLIDO_USUARIO rowType:XLFormRowDescriptorTypeName title:@"Apellido"];
    [row.cellConfigAtConfigure setObject:@"Apellido" forKey:@"textField.placeholder"];
    [row.cellConfigAtConfigure setObject:@(NSTextAlignmentRight) forKey:@"textField.textAlignment"];
    row.required = YES;
    [section addFormRow:row];
    
    // Seccion contrasenia
    section = [XLFormSectionDescriptor formSectionWithTitle:@"Contraseña"];
    section.footerTitle = @"Su contraseña debe tener al menos 8 caracteres y al menos un número y una letra";
    [form addFormSection:section];

    row = [XLFormRowDescriptor formRowDescriptorWithTag:KEY_CONTRASENIA rowType:XLFormRowDescriptorTypePassword title:@"Contraseña"];
    [row.cellConfigAtConfigure setObject:@"Contraseña" forKey:@"textField.placeholder"];
    [row.cellConfigAtConfigure setObject:@(NSTextAlignmentRight) forKey:@"textField.textAlignment"];
    row.required = YES;
    [row addValidator:[XLFormRegexValidator formRegexValidatorWithMsg:@"Su contraseña debe tener al menos 8 caracteres y al menos un número y una letra" regex:kRegexContrasenia]];
    [section addFormRow:row];
    
    // Seccion informacion opcional
    section = [XLFormSectionDescriptor formSectionWithTitle:@"Datos adicionales"];
    [form addFormSection:section];
    
    row = [XLFormRowDescriptor formRowDescriptorWithTag:KEY_FECHA_NACIMIENTO rowType:XLFormRowDescriptorTypeDate title:@"Fecha de Nacimiento"];
    row.value = [NSDate new];
    [section addFormRow:row];
    
    row = [XLFormRowDescriptor formRowDescriptorWithTag:KEY_DNI rowType:XLFormRowDescriptorTypeNumber title:@"D.N.I."];
    [row.cellConfigAtConfigure setObject:@"D.N.I." forKey:@"textField.placeholder"];
    [row.cellConfigAtConfigure setObject:@(NSTextAlignmentRight) forKey:@"textField.textAlignment"];
    [row addValidator:[XLFormRegexValidator formRegexValidatorWithMsg:@"Ingresar solo numeros" regex:kRegexDNI]];
    [row.cellConfigAtConfigure setObject:@(8) forKey:@"textFieldMaxNumberOfCharacters"];
    [section addFormRow:row];
    
    row = [XLFormRowDescriptor formRowDescriptorWithTag:KEY_CUIT rowType:XLFormRowDescriptorTypeText title:@"C.U.I.T."];
    [row.cellConfigAtConfigure setObject:@"C.U.I.T." forKey:@"textField.placeholder"];
    [row.cellConfigAtConfigure setObject:@(NSTextAlignmentRight) forKey:@"textField.textAlignment"];
    [row addValidator:[XLFormRegexValidator formRegexValidatorWithMsg:@"C.U.I.T debe llevar guiones" regex:kRegexCUIT]];
    [row.cellConfigAtConfigure setObject:@(13) forKey:@"textFieldMaxNumberOfCharacters"];
    [section addFormRow:row];
    
    row = [XLFormRowDescriptor formRowDescriptorWithTag:KEY_DOMICILIO rowType:XLFormRowDescriptorTypeText title:@"Domicilio"];
    [row.cellConfigAtConfigure setObject:@"Domicilio" forKey:@"textField.placeholder"];
    [row.cellConfigAtConfigure setObject:@(NSTextAlignmentRight) forKey:@"textField.textAlignment"];
    [row.cellConfigAtConfigure setObject:@(50) forKey:@"textFieldMaxNumberOfCharacters"];
    [section addFormRow:row];
    
    self.form = form;
}

-(BOOL)validarDatos {
    
    NSArray *formValidationErrors = [self formValidationErrors];
    if ([formValidationErrors count] > 0) {
        for (NSError *error in formValidationErrors) {
            
             XLFormValidationStatus * validationStatus = [[error userInfo] objectForKey:XLValidationStatusErrorKey];
            
            if ([validationStatus.rowDescriptor.tag isEqualToString:KEY_USUARIO]){
                [self markInvalidRowAtIndexPath:[self.form indexPathOfFormRow:validationStatus.rowDescriptor]];
            }
            else if ([validationStatus.rowDescriptor.tag isEqualToString:KEY_EMAIL]){
                [self markInvalidRowAtIndexPath:[self.form indexPathOfFormRow:validationStatus.rowDescriptor]];
            }
            else if ([validationStatus.rowDescriptor.tag isEqualToString:KEY_NOMBRE_USUARIO]){
                [self markInvalidRowAtIndexPath:[self.form indexPathOfFormRow:validationStatus.rowDescriptor]];
            }
            else if ([validationStatus.rowDescriptor.tag isEqualToString:KEY_APELLIDO_USUARIO]){
                [self markInvalidRowAtIndexPath:[self.form indexPathOfFormRow:validationStatus.rowDescriptor]];
            }
            else if ([validationStatus.rowDescriptor.tag isEqualToString:KEY_CONTRASENIA]){
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
    [self registrarUsuario];
}

#pragma mark - Acciones form

- (IBAction)enviarDatos:(UIBarButtonItem *)sender {
    [self enviarForm];
}

@end
