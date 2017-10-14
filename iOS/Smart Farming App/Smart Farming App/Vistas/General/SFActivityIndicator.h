//
//  SMActivityIndicator.h
//  Smart Farming App
//
//  Created by Facundo Palma on 10/9/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <UIKit/UIKit.h>
#import <Foundation/Foundation.h>

@interface SFActivityIndicator : UIView

@property (nonatomic, strong) UIActivityIndicatorView *activityIndicator;

#pragma mark - Inicializacion

+ (instancetype) instance;
- (instancetype) initWithFrame:(CGRect)frame;

@end
