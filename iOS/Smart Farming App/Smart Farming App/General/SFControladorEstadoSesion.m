//
//  SFControladorEstadoSesion.m
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/19/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <UIKit/UIKit.h>

#import "SFControladorEstadoSesion.h"

#import "IdentificadoresSegue.h"
#import "SFActivityIndicator.h"
#import "ContextoUsuario.h"

@implementation SFControladorEstadoSesion

-(void)forzarCierreSesion {
    [[ContextoUsuario instance] invalidateContext];
    
    UIAlertController *sesionFinalizadaAlert = [UIAlertController alertControllerWithTitle:@"Sesion invalida" message:@"Necesita volver a ingresar para continuar" preferredStyle:UIAlertControllerStyleAlert];
    
    UIAlertAction *aceptarAction = [UIAlertAction actionWithTitle:@"Aceptar" style:UIAlertActionStyleDefault handler:^(UIAlertAction * _Nonnull action) {
        [[[[UIApplication sharedApplication] delegate] window].rootViewController dismissViewControllerAnimated:YES completion:nil];
        [self performSelector:@selector(irAPaginaInicio) withObject:nil afterDelay:0.50];
    }];
    
    [sesionFinalizadaAlert addAction:aceptarAction];
    
    [self hideActivityIndicator];
    [[[[UIApplication sharedApplication] delegate] window].rootViewController presentViewController:sesionFinalizadaAlert animated:YES completion:nil];
}

-(void)irAPaginaInicio {
    
    if ([[[[UIApplication sharedApplication] delegate] window].rootViewController navigationController]) {
        [[[[[UIApplication sharedApplication] delegate] window].rootViewController navigationController] performSegueWithIdentifier:kSFNavegarEstadoNoAutenticadoSegue sender:[[[UIApplication sharedApplication] delegate] window].rootViewController];
    } else {
        UINavigationController *navigationController = (UINavigationController *)[[[UIApplication sharedApplication] delegate] window].rootViewController;
        [navigationController popToRootViewControllerAnimated:YES];
    }
}

-(void)hideActivityIndicator {
    dispatch_async(dispatch_get_main_queue(), ^{
        if ([[SFActivityIndicator instance] isDescendantOfView:[[[UIApplication sharedApplication] delegate] window]]) {
            [[SFActivityIndicator instance] removeFromSuperview];
        }
    });
}

@end
