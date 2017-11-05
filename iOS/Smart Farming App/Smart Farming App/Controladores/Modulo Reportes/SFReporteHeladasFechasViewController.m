//
//  SFReporteHeladasFechasViewController.m
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/31/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFReporteHeladasFechasViewController.h"

#import "SFReporteHeladasOcurrenciasViewController.h"

@interface SFReporteHeladasFechasViewController ()

@end

@implementation SFReporteHeladasFechasViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view.
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

// In a storyboard-based application, you will often want to do a little preparation before navigation
- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender {
    // Get the new view controller using [segue destinationViewController].
    // Pass the selected object to the new view controller.
    
    if ([[segue identifier] isEqualToString:kSFNavegarAReporteHeladasEventosSegue])
    {
        // Get reference to the destination view controller
        SFReporteHeladasOcurrenciasViewController *vc = [segue destinationViewController];
        
        NSDictionary *values = [self.form formValues];
        
        // Pass any objects to the view controller here, like...
        vc.idSector = self.idSector;
        vc.fechaInicioSector = [values objectForKey:@"fecha_inicial"];;
        vc.fechaFinSector = [values objectForKey:@"fecha_final"];;
    }
}

#pragma mark - Formulario

-(void)initializeForm {
    
    XLFormDescriptor * form;
    XLFormSectionDescriptor * section;
    XLFormRowDescriptor * row;
    
    form = [XLFormDescriptor formDescriptorWithTitle:@"Seleccionar rango fechas"];
    
    // Seccion informacion obligatoria
    section = [XLFormSectionDescriptor formSectionWithTitle:@""];
    [form addFormSection:section];
    
    row = [XLFormRowDescriptor formRowDescriptorWithTag:@"fecha_inicial" rowType:XLFormRowDescriptorTypeDate title:@"Fecha inicial"];
    row.value = [NSDate new];
    row.required = YES;
    [section addFormRow:row];
    
    row = [XLFormRowDescriptor formRowDescriptorWithTag:@"fecha_final" rowType:XLFormRowDescriptorTypeDate title:@"Fecha final"];
    row.value = [NSDate new];
    
    [section addFormRow:row];
    
    self.form = form;
}

-(BOOL)validarDatos {
    
    NSArray *formValidationErrors = [self formValidationErrors];
    if ([formValidationErrors count] > 0) {
        
        return NO;
    }
    return YES;
}

-(void)hacerLlamadaServicio {
    [self performSegueWithIdentifier:kSFNavegarAReporteHeladasEventosSegue sender:self];
}

#pragma mark - Acciones form

- (IBAction)enviarDatos:(UIBarButtonItem *)sender {
    [self enviarForm];
}

@end
