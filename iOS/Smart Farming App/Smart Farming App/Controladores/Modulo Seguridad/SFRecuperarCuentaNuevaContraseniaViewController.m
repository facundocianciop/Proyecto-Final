//
//  SFRecuperarCuentaNuevaContraseniaViewController.m
//  Smart Farming App
//
//  Created by Facundo Palma on 10/17/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFRecuperarCuentaNuevaContraseniaViewController.h"

#import "ServiciosModuloSeguridad.h"

@interface SFRecuperarCuentaNuevaContraseniaViewController ()

@end

@implementation SFRecuperarCuentaNuevaContraseniaViewController

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



#pragma mark - Formulario

-(void)initializeForm {
    
    XLFormDescriptor * form;
    XLFormSectionDescriptor * section;
    XLFormRowDescriptor * row;
    
    form = [XLFormDescriptor formDescriptorWithTitle:@"Código de verificación"];
    
    // Seccion contrasenia
    section = [XLFormSectionDescriptor formSectionWithTitle:@"Contraseña"];
    section.footerTitle = @"Su contraseña debe tener al menos 8 caracteres y al menos un número y una letra";
    [form addFormSection:section];
    
    row = [XLFormRowDescriptor formRowDescriptorWithTag:KEY_CODIGO_VERIFICACION rowType:XLFormRowDescriptorTypePassword title:@"Código verificación"];
    [row.cellConfigAtConfigure setObject:@"Código" forKey:@"textField.placeholder"];
    [row.cellConfigAtConfigure setObject:@(NSTextAlignmentRight) forKey:@"textField.textAlignment"];
    row.required = YES;
    [section addFormRow:row];
    
    row = [XLFormRowDescriptor formRowDescriptorWithTag:KEY_CONTRASENIA_NUEVA rowType:XLFormRowDescriptorTypePassword title:@"Contraseña"];
    [row.cellConfigAtConfigure setObject:@"Contraseña" forKey:@"textField.placeholder"];
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
            
            if ([validationStatus.rowDescriptor.tag isEqualToString:KEY_CODIGO_VERIFICACION]){
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
    

}

#pragma mark - Acciones form

- (IBAction)enviarDatos:(id)sender {
    [self enviarForm];
}

@end
