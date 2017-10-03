//
//  PantallaActivityIndicator.m
//  proyectoRiego2017
//
//  Created by Facundo José Palma on 9/21/17.
//  Copyright © 2017 Facundo José Palma. All rights reserved.
//

#import "PRPantallaActivityIndicator.h"

@implementation PRPantallaActivityIndicator

#pragma mark - Initialization

+(instancetype) instance {
    static PRPantallaActivityIndicator *loadingView = nil;
    static dispatch_once_t token;
    dispatch_once(&token, ^{
        loadingView = [[self alloc] initWithFrame:[UIScreen mainScreen].bounds];
    });
    return loadingView;
}

-(instancetype)initWithFrame:(CGRect)frame {
    
    if (self = [super initWithFrame:frame]) {
        [self setBackgroundColor:[UIColor blackColor]];
        [self setAlpha:0.6f];
        
        self.activityIndicator = [[UIActivityIndicatorView alloc] initWithActivityIndicatorStyle:UIActivityIndicatorViewStyleWhiteLarge];
        [self.activityIndicator setCenter:CGPointMake([UIScreen mainScreen].bounds.size.width/2, [UIScreen mainScreen].bounds.size.height/2)];
        
        [self addSubview:self.activityIndicator];
    }
    return self;
}

#pragma mark - Overrides

-(void) didMoveToSuperview {
    if ([self superview]) {
        [self.activityIndicator startAnimating];
    } else {
        [self.activityIndicator stopAnimating];
    }
}

@end
