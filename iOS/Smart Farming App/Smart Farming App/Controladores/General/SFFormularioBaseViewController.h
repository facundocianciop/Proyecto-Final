//
//  SFFormularioBaseViewController.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/12/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <XLFormViewController.h>
#import <XLForm.h>

#import "SFUtils.h"
#import "SFConstantesComunes.h"
#import "IdentificadoresSegue.h"

@interface SFFormularioBaseViewController : XLFormViewController

// Form actions
-(void)initializeForm;
-(void)enviarForm;
-(BOOL)validarDatos;
-(void)hacerLlamadaServicio;
-(void)markInvalidRowAtIndexPath:(NSIndexPath *)indexPath;

// Activity indicator for async service operations
-(void)showActivityIndicator;
-(void)hideActivityIndicator;

// Handle errors
-(void)handleError:(NSError *)error;

// Handle error with custom message
-(void)handleErrorWithPromptTitle:(NSString *)title message:(NSString *)message withCompletion:(void(^)(void))completionblock;

// Show custom information message
-(void)userInformationPrompt:(NSString *)message;

@end
