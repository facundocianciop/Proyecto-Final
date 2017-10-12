//
//  SFFormularioBaseViewController.m
//  Smart Farming App
//
//  Created by Facundo Palma on 10/11/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFFormularioBaseViewController.h"
#import "SFTextField.h"
#import <Masonry.h>

@interface SFFormularioBaseViewController ()

@property (nonatomic, strong) UIGestureRecognizer *tapRecognizer;

@end

@implementation SFFormularioBaseViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view.
    
    self.textFieldsArray = [NSMutableArray new];
    
    self.viewScrollView.keyboardDismissMode = UIScrollViewKeyboardDismissModeInteractive;
    self.automaticallyAdjustsScrollViewInsets = NO;
    
    self.tapRecognizer = [[UITapGestureRecognizer alloc] initWithTarget:self action:@selector(dismissKeyboard)];
    [self.view addGestureRecognizer:self.tapRecognizer];
}

- (void)viewWillAppear:(BOOL)animated {
    [super viewWillAppear:animated];
    
    [[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(keyboardWillShow:) name:UIKeyboardWillShowNotification object:nil];
    [[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(keyboardWillHide:) name:UIKeyboardWillHideNotification object:nil];
}

- (void)viewWillDisappear:(BOOL)animated {
    [super viewWillDisappear:animated];
    
    [[NSNotificationCenter defaultCenter] removeObserver:self name:UIKeyboardWillShowNotification object:nil];
    [[NSNotificationCenter defaultCenter] removeObserver:self name:UIKeyboardWillHideNotification object:nil];
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    
    [self.view removeGestureRecognizer:self.tapRecognizer];
}

-(void)dealloc {
    [self.view removeGestureRecognizer:self.tapRecognizer];
}

#pragma mark - Public

-(void)dismissKeyboard {
    [self.view endEditing:YES];
}

-(BOOL) areFieldsValid {
    
    NSArray *invalidFields = [self getInvalidFields];
    
    if (invalidFields.count) {
        UIAlertController *invalidFieldAlert =[UIAlertController alertControllerWithTitle:@"" message:[self getInvalidFieldMessage:invalidFields] preferredStyle:UIAlertControllerStyleAlert];
        
        UIAlertAction *okAction = [UIAlertAction actionWithTitle:@"Aceptar" style:UIAlertActionStyleDefault handler:^(UIAlertAction * _Nonnull action) {
            [[invalidFields firstObject] becomeFirstResponder];
        }];
        
        [invalidFieldAlert addAction:okAction];
        
        [self presentViewController:invalidFieldAlert animated:YES completion:nil];
        
        return NO;
    }
    
    return YES;
}

-(BOOL) isTextViewValid:(UITextView *)textView {
    NSCharacterSet *set = [NSCharacterSet whitespaceCharacterSet];
    
    if (([[textView.text stringByTrimmingCharactersInSet:set] length] == 0)){
        
        UIAlertController *invalidFieldAlert =[UIAlertController alertControllerWithTitle:@"" message:@"Por favor ingrese sus comentarios" preferredStyle:UIAlertControllerStyleAlert];
        
        UIAlertAction *okAction = [UIAlertAction actionWithTitle:@"Aceptar" style:UIAlertActionStyleDefault handler:^(UIAlertAction * _Nonnull action) {
            [textView becomeFirstResponder];
        }];
        
        [invalidFieldAlert addAction:okAction];
        [self presentViewController:invalidFieldAlert animated:YES completion:nil];
        return NO;
    }
    return YES;
}

#pragma mark - Private

-(NSArray *)getInvalidFields {
    NSMutableArray *invalidFields = [NSMutableArray new];
    
    for (SFTextField *textField in self.textFieldsArray) {
        if (![textField isInputValid]) {
            [invalidFields addObject:textField];
        }
    }
    
    return invalidFields;
}

-(NSString *)getInvalidFieldMessage:(NSArray *)invalidFields {
    
    SFTextField *textField = (SFTextField *)[invalidFields firstObject];
    
    return textField.invalidFieldMessage;
}

#pragma mark - Keyboard handling

-(void) keyboardWillShow:(NSNotification *)notification {
    
    NSDictionary* info = [notification userInfo];
    CGSize kbSize = [[info objectForKey:UIKeyboardFrameBeginUserInfoKey] CGRectValue].size;
    CGSize tabBarSize = self.tabBarController.tabBar.frame.size;
    
    CGFloat keyboardHeight = kbSize.height - tabBarSize.height;
    
    [UIView animateWithDuration:0.3 animations:^{
        [self.viewScrollView mas_updateConstraints:^(MASConstraintMaker *make){
            make.bottom.equalTo(self.view.mas_bottom).with.offset(-keyboardHeight);
        }];
        
        [self.view layoutIfNeeded];
    }];
}

-(void)keyboardWillHide:(NSNotification *)notification {
    
    [UIView animateWithDuration:0.3 animations:^{
        
        [self.viewScrollView mas_updateConstraints:^(MASConstraintMaker *make){
            make.bottom.equalTo(self.view.mas_bottom);
        }];
        
        [self.view layoutIfNeeded];
    }];
}


#pragma mark - UITextFieldDelegate

-(BOOL)textField:(SFTextField *)textField shouldChangeCharactersInRange:(NSRange)range replacementString:(NSString *)string {
    
    if(range.length + range.location > textField.text.length) {
        return NO;
    }
    
    if (textField.style == SFTextFieldStyleCuit) {
        if ([string rangeOfCharacterFromSet:[NSCharacterSet decimalDigitCharacterSet].invertedSet].location != NSNotFound) {
            return NO;
        }
        
        NSUInteger newLength = [textField.text length] + [string length] - range.length;
        return newLength <= 11;
    }
    
    if (textField.style == SFTextFieldStyleTelefono) {
        if ([string rangeOfCharacterFromSet:[NSCharacterSet characterSetWithCharactersInString:@"0123456789+*#-() "].invertedSet].location != NSNotFound) {
            return NO;
        }
    }
    
    return YES;
}

#pragma mark - UITextViewDelegate

-(BOOL)textView:(UITextView *)textView shouldChangeTextInRange:(NSRange)range replacementText:(NSString *)text {
    
    return textView.text.length + (text.length - range.length) <= 300;
}
@end
