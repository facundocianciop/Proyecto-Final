//
//  SFNavegarEstadoNoAutenticadoSegue.m
//  Smart Farming App
//
//  Created by Facundo Palma on 10/16/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFNavegarEstadoNoAutenticadoSegue.h"

#import "SFInicioSesionViewController.h"

@implementation SFNavegarEstadoNoAutenticadoSegue

-(void)perform {
    UIViewController *source = (UIViewController *)self.sourceViewController;
    
    SFInicioSesionViewController *destino = [SFInicioSesionViewController new];
    source.view.window.rootViewController = destino;
}

@end
