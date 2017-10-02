//
//  ControladorBase.h
//  proyectoRiego2017
//
//  Created by Facundo José Palma on 9/21/17.
//  Copyright © 2017 Facundo José Palma. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <UIKit/UIKit.h>

#import "PRUtils.h"
#import "PRConstantesComunes.h"

@interface PRViewControllerBase : UIViewController

#pragma mark - Public Controller Utiltity

// Activity indicator for async service operations

-(void)showActivityIndicator;
-(void)hideActivityIndicator;

// Handle services returning no records

-(void)handleNoRecords;

// Handle errors

-(void)handleError:(NSError *)error;

// Handle error with custom message

-(void)handleErrorWithPrompt:(NSString *)message;

// Show custom information message

-(void)userInformationPrompt:(NSString *)message;

@end
