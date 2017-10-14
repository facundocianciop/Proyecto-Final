//
//  SFTextField.m
//  Smart Farming App
//
//  Created by Facundo Palma on 10/11/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFTextField.h"
#import "SFUtils.h"

@implementation SFTextField

- (instancetype)init {
    return [self initWithStyle:SFTextFieldStyleNone];
}

-(instancetype)initWithStyle:(SFTextFieldStyle) style {
    
    self = [super init];
    if (self) {
        [self configureTextField];
        [self configurePropertiesBasedOnStyle:(SFTextFieldStyle)style];
    }
    return self;
}

-(void) configureTextField {
    
    self.font = [UIFont systemFontOfSize:[UIFont labelFontSize]];
    self.autocorrectionType = UITextAutocorrectionTypeNo;
}

- (void) configurePropertiesBasedOnStyle:(SFTextFieldStyle)style {
    
    self.style = style;
    
    switch (self.style) {
            
        case SFTextFieldStyleUsuario:
            self.placeholder = @"Usuario";
            self.autocapitalizationType = UITextAutocapitalizationTypeNone;
            self.keyboardType = UIKeyboardTypeEmailAddress;
            break;
            
        case SFTextFieldStylePassword:
            self.placeholder = @"Contraseña";
            self.secureTextEntry = YES;
            self.keyboardType = UIKeyboardTypeDefault;
            break;
            
        case SFTextFieldStyleEmail:
            self.placeholder = @"E-mail";
            self.autocapitalizationType = UITextAutocapitalizationTypeNone;
            self.keyboardType = UIKeyboardTypeEmailAddress;
            self.invalidFieldMessage = @"Por favor complete el E-mail correctamente";
            break;
            
        case SFTextFieldStyleCuit:
            self.placeholder = @"Cuit/Cuil";
            self.keyboardType = UIKeyboardTypeNumberPad;
            self.invalidFieldMessage = @"Por favor complete el Cuit/Cuil";
            break;
            
        case SFTextFieldStyleTelefono:
            self.placeholder = @"Teléfono";
            self.keyboardType = UIKeyboardTypePhonePad;
            self.invalidFieldMessage = @"Por favor complete el Teléfono";
            break;
            
        case SFTextFieldStyleDomicilio:
            self.placeholder = @"Domicilio";
            self.keyboardType = UIKeyboardTypeDefault;
            self.invalidFieldMessage = @"Por favor complete el domicilio";
            break;
            
        default:
            self.placeholder = @"Campo no definido";
            self.keyboardType = UIKeyboardTypeDefault;
            break;
    }
}

#pragma mark - Public

-(BOOL)isInputValid {
    
    BOOL valid = NO;
    NSCharacterSet *set = [NSCharacterSet whitespaceCharacterSet];
    
    switch (self.style) {
            
        case SFTextFieldStyleUsuario:
            valid = YES;
            break;
            
        case SFTextFieldStylePassword:
            valid = YES;
            break;
            
        case SFTextFieldStyleCuit:
            
            if (!([[self.text stringByTrimmingCharactersInSet:set] length] == 0)){
                valid = YES;
            }
            
            break;
            
        case SFTextFieldStyleEmail:
            
            if (!([[self.text stringByTrimmingCharactersInSet:set] length] == 0)){
                valid = [self isEmailValid:self.text];
            }
            break;
            
        case SFTextFieldStyleTelefono:
            
            if (!([[self.text stringByTrimmingCharactersInSet:set] length] == 0)){
                valid = YES;
            }
            break;
            
        case SFTextFieldStyleDomicilio:
            
            if (!([[self.text stringByTrimmingCharactersInSet:set] length] == 0)){
                valid = YES;
            }
            break;
            
        default:
            break;
    }
    return valid;
}

#pragma mark - Private

-(BOOL) isEmailValid:(NSString *)checkString {
    BOOL stricterFilter = NO;
    NSString *stricterFilterString = @"^[A-Z0-9a-z\\._%+-]+@([A-Za-z0-9-]+\\.)+[A-Za-z]{2,4}$";
    NSString *laxString = @"^.+@([A-Za-z0-9-]+\\.)+[A-Za-z]{2}[A-Za-z]*$";
    NSString *emailRegex = stricterFilter ? stricterFilterString : laxString;
    NSPredicate *emailTest = [NSPredicate predicateWithFormat:@"SELF MATCHES %@", emailRegex];
    return [emailTest evaluateWithObject:checkString];
}

@end
