//
//  SFFormularioBaseViewController.h
//  Smart Farming App
//
//  Created by Facundo Palma on 10/11/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFViewControllerBase.h"

@interface SFFormularioBaseViewController : SFViewControllerBase <UITextFieldDelegate, UIScrollViewDelegate, UITextViewDelegate>

@property (strong, nonatomic) UIScrollView* viewScrollView;
@property (strong, nonatomic) NSMutableArray *textFieldsArray;

#pragma mark - Public

-(void)dismissKeyboard;

-(BOOL) areFieldsValid;
-(BOOL) isTextViewValid:(UITextView *)textView;

@end
