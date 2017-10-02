//
//  PantallaActivityIndicator.h
//  proyectoRiego2017
//
//  Created by Facundo José Palma on 9/21/17.
//  Copyright © 2017 Facundo José Palma. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface PRPantallaActivityIndicator : UIView

@property (nonatomic, strong) UIActivityIndicatorView *activityIndicator;

#pragma mark - Inicializacion

+ (instancetype) instance;
- (instancetype) initWithFrame:(CGRect)frame;

@end
