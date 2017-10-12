//
//  SFNavegarEstadoAutenticadoSegue.m
//  Smart Farming App
//
//  Created by Facundo Palma on 10/12/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFNavegarEstadoAutenticadoSegue.h"

@implementation SFNavegarEstadoAutenticadoSegue

-(void)perform {
    
    UIViewController *sourceViewController = (UIViewController*)[self sourceViewController];
    UIViewController *destinationController = (UIViewController*)[self destinationViewController];
    
    [sourceViewController.navigationController setViewControllers: [NSArray arrayWithObject: destinationController] animated: YES];
}

@end
