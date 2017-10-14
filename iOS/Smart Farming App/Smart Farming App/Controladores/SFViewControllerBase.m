//
//  SFViewControllerBase.m
//  Smart Farming App
//
//  Created by Facundo Palma on 10/9/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFViewControllerBase.h"

#import "SFActivityIndicator.h"

@interface SFViewControllerBase ()

@property (nonatomic, strong) SFActivityIndicator *activityIndicatorView;

@property (nonatomic, assign) BOOL                    promptDisplayed;
@property (nonatomic, strong) UIAlertController       *userPrompt;
@property (nonatomic, strong) UIAlertAction           *primaryAction;
@property (nonatomic, strong) UIAlertAction           *secondaryAction;

@end

NSString *const kBCDefaultPrimaryAction     = @"Aceptar";
NSString *const kBCDefaultSecondaryAction   = @"Cancelar";
NSString *const kBCNoItemsError             = @"No se encontraron resultados para esta solicitud.";

@implementation SFViewControllerBase

- (instancetype)initWithCoder:(NSCoder *)coder
{
    self = [super initWithCoder:coder];
    if (self) {
        _activityIndicatorView = [SFActivityIndicator instance];
    }
    return self;
}

-(void)viewDidLoad {
    [super viewDidLoad];
    
    UIBarButtonItem *backButton = [[UIBarButtonItem alloc]initWithTitle:kSFNavigationBarBackButtonText style:UIBarButtonItemStylePlain target:nil action:nil];
    [self.navigationItem setBackBarButtonItem:backButton];
}

#pragma mark - Public Controller Utiltity

-(void)showActivityIndicator {
    __weak SFViewControllerBase *weakSelf = self;
    
    dispatch_async(dispatch_get_main_queue(), ^{
        [[[[UIApplication sharedApplication] delegate] window] addSubview:weakSelf.activityIndicatorView];
    });
}

-(void)hideActivityIndicator {
    __weak SFViewControllerBase *weakSelf = self;
    
    dispatch_async(dispatch_get_main_queue(), ^{
        [weakSelf.activityIndicatorView removeFromSuperview];
    });
}

// Manejar servicios sin respuesta
-(void)handleNoRecords {
    
    self.userPrompt = [UIAlertController alertControllerWithTitle:@"" message:kBCNoItemsError preferredStyle:UIAlertControllerStyleAlert];
    
    __weak SFViewControllerBase *weakSelf = self;
    self.primaryAction = [UIAlertAction actionWithTitle:kBCDefaultPrimaryAction style:UIAlertActionStyleDefault handler:^(UIAlertAction * _Nonnull action) {
        weakSelf.promptDisplayed = NO;
        weakSelf.userPrompt = nil;
        weakSelf.primaryAction = nil;
    }];
    
    [self.userPrompt addAction:self.primaryAction];
    
    [self showPrompt];
    
}

// Manejar errores
-(void)handleError:(NSError *)error {
    NSString *errorDescription = [error localizedDescription];
    
    self.userPrompt = [UIAlertController alertControllerWithTitle:@"Error" message:errorDescription preferredStyle:UIAlertControllerStyleAlert];
    
    __weak SFViewControllerBase *weakSelf = self;
    self.primaryAction = [UIAlertAction actionWithTitle:kBCDefaultPrimaryAction style:UIAlertActionStyleDefault handler:^(UIAlertAction * _Nonnull action) {
        weakSelf.promptDisplayed = NO;
        weakSelf.userPrompt = nil;
        weakSelf.primaryAction = nil;
    }];
    
    [self.userPrompt addAction:self.primaryAction];
    
    [self showPrompt];
}

// Manejar error con mensaje
-(void)handleErrorWithPromptTitle:(NSString *)title message:(NSString *)message {
    
    self.userPrompt = [UIAlertController alertControllerWithTitle:title message:message preferredStyle:UIAlertControllerStyleAlert];
    
    __weak SFViewControllerBase *weakSelf = self;
    self.primaryAction = [UIAlertAction actionWithTitle:kBCDefaultPrimaryAction style:UIAlertActionStyleDefault handler:^(UIAlertAction * _Nonnull action) {
        weakSelf.promptDisplayed = NO;
        weakSelf.userPrompt = nil;
        weakSelf.primaryAction = nil;
    }];
    
    [self.userPrompt addAction:self.primaryAction];
    
    [self showPrompt];
}

// Mostrar mensaje con informacion
-(void)userInformationPrompt:(NSString *)message {
    self.userPrompt = [UIAlertController alertControllerWithTitle:@"" message:message preferredStyle:UIAlertControllerStyleAlert];
    
    __weak SFViewControllerBase *weakSelf = self;
    self.primaryAction = [UIAlertAction actionWithTitle:kBCDefaultPrimaryAction style:UIAlertActionStyleDefault handler:^(UIAlertAction * _Nonnull action) {
        weakSelf.promptDisplayed = NO;
        weakSelf.userPrompt = nil;
        weakSelf.primaryAction = nil;
    }];
    
    [self.userPrompt addAction:self.primaryAction];
    
    [self showPrompt];
}

#pragma mark - Interal

-(void)showPrompt {
    
    if (self.userPrompt && !self.promptDisplayed)
    {
        __weak SFViewControllerBase *weakSelf = self;
        [self presentViewController:self.userPrompt animated:YES completion:^{
            weakSelf.promptDisplayed = YES;
        }];
    }
    
}

@end
