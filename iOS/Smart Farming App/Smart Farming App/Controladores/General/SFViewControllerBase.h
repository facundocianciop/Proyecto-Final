//
//  SFViewControllerBase.h
//  Smart Farming App
//
//  Created by Facundo Palma on 10/9/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <UIKit/UIKit.h>

#import "SFUtils.h"
#import "SFConstantesComunes.h"
#import "IdentificadoresSegue.h"

@interface SFViewControllerBase : UIViewController

#pragma mark - Public Controller Utiltity

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
