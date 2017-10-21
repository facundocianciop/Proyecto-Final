//
//  SFModificarUsuarioViewController.h
//  Smart Farming App
//
//  Created by Facundo Palma on 10/17/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFFormularioBaseViewController.h"

@interface SFModificarUsuarioViewController : SFFormularioBaseViewController

@property (strong, nonatomic) XLFormRowDescriptor *emailRow;
@property (strong, nonatomic) XLFormRowDescriptor *nombreRow;
@property (strong, nonatomic) XLFormRowDescriptor *apellidoRow;
@property (strong, nonatomic) XLFormRowDescriptor *fechaNacimientoRow;
@property (strong, nonatomic) XLFormRowDescriptor *dniRow;
@property (strong, nonatomic) XLFormRowDescriptor *cuitRow;
@property (strong, nonatomic) XLFormRowDescriptor *domicilioRow;

@end
