//
//  SFNavegarASeccionFincaSegue.m
//  Smart Farming App
//
//  Created by Facundo Palma on 10/15/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFNavegarASeccionFincaSegue.h"
#import "AppDelegate.h"

@implementation SFNavegarASeccionFincaSegue

-(void)perform {
    UIViewController *source = (UIViewController *)self.sourceViewController;
    source.view.window.rootViewController = self.destinationViewController;
}

@end
