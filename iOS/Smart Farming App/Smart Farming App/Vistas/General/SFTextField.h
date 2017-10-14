//
//  SFTextField.h
//  Smart Farming App
//
//  Created by Facundo Palma on 10/11/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <UIKit/UIKit.h>

typedef NS_ENUM(NSInteger, SFTextFieldStyle) {
    SFTextFieldStyleUsuario,
    SFTextFieldStylePassword,
    SFTextFieldStyleEmail,
    SFTextFieldStyleDNI,
    SFTextFieldStyleTelefono,
    SFTextFieldStyleCuit,
    SFTextFieldStyleDomicilio,
    SFTextFieldStyleNone
};

@interface SFTextField : UITextField

@property (strong, nonatomic) NSString *invalidFieldMessage;
@property (assign, nonatomic) SFTextFieldStyle style;

-(instancetype)initWithStyle:(SFTextFieldStyle) style;

-(BOOL)isInputValid;

@end
