//
//  SFFormularioBaseViewController.m
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/12/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFFormularioBaseViewController.h"

#import "SFActivityIndicator.h"

@interface SFFormularioBaseViewController ()

@property (nonatomic, strong) SFActivityIndicator *activityIndicatorView;

@property (nonatomic, assign) BOOL                    promptDisplayed;
@property (nonatomic, strong) UIAlertController       *userPrompt;
@property (nonatomic, strong) UIAlertAction           *primaryAction;
@property (nonatomic, strong) UIAlertAction           *secondaryAction;

@end

@implementation SFFormularioBaseViewController

- (instancetype)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil {
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self){
         _activityIndicatorView = [SFActivityIndicator instance];
        [self initializeForm];
    }
    return self;
}

- (instancetype)initWithCoder:(NSCoder *)coder {
    self = [super initWithCoder:coder];
    if (self) {
        _activityIndicatorView = [SFActivityIndicator instance];
        [self initializeForm];
    }
    return self;
}

- (void)viewDidLoad {
    [super viewDidLoad];
    
    UIBarButtonItem *backButton = [[UIBarButtonItem alloc]initWithTitle:@"" style:UIBarButtonItemStylePlain target:nil action:nil];
    [self.navigationItem setBackBarButtonItem:backButton];
    
    self.tableView.tintColor = [SFUtils primaryColor];
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

#pragma mark - Form Actions

-(void)initializeForm {
    [NSException raise:@"Invoked abstract method" format:@"Invoked abstract method"];
}

-(BOOL)validarDatos {
    [NSException raise:@"Invoked abstract method" format:@"Invoked abstract method"];
    return NO;
}

-(void)hacerLlamadaServicio {
    [NSException raise:@"Invoked abstract method" format:@"Invoked abstract method"];
}

-(void)enviarForm {
    if ([self validarDatos]) {
        [self hacerLlamadaServicio];
    }
}

-(void)markInvalidRowAtIndexPath:(NSIndexPath *)indexPath {
    UITableViewCell * cell = [self.tableView cellForRowAtIndexPath:indexPath];
    [self animateCell:cell];
}

-(void)animateCell:(UITableViewCell *)cell {
    
    cell.backgroundColor = [SFUtils formCellErrorColor];
    
    CAKeyframeAnimation *animation = [CAKeyframeAnimation animation];
    animation.keyPath = @"position.x";
    animation.values =  @[ @0, @20, @-20, @10, @0];
    animation.keyTimes = @[@0, @(1 / 6.0), @(3 / 6.0), @(5 / 6.0), @1];
    animation.duration = 0.3;
    animation.timingFunction = [CAMediaTimingFunction functionWithName:kCAMediaTimingFunctionEaseOut];
    animation.additive = YES;
    
    [cell.layer addAnimation:animation forKey:@"shake"];
    
    [UIView animateWithDuration:0.3 animations:^{
        cell.backgroundColor = [SFUtils formCellColor];
    }];
}

#pragma mark - Public Controller Utiltity

-(void)showActivityIndicator {
    __weak SFFormularioBaseViewController *weakSelf = self;
    
    dispatch_async(dispatch_get_main_queue(), ^{
        [[[[UIApplication sharedApplication] delegate] window] addSubview:weakSelf.activityIndicatorView];
    });
}

-(void)hideActivityIndicator {
    __weak SFFormularioBaseViewController *weakSelf = self;
    
    dispatch_async(dispatch_get_main_queue(), ^{
        [weakSelf.activityIndicatorView removeFromSuperview];
    });
}

// Manejar errores
-(void)handleError:(NSError *)error {
    NSString *errorDescription = [error localizedDescription];
    
    self.userPrompt = [UIAlertController alertControllerWithTitle:@"Error" message:errorDescription preferredStyle:UIAlertControllerStyleAlert];
    
    __weak SFFormularioBaseViewController *weakSelf = self;
    self.primaryAction = [UIAlertAction actionWithTitle:kSFDefaultPrimaryAction style:UIAlertActionStyleDefault handler:^(UIAlertAction * _Nonnull action) {
        weakSelf.promptDisplayed = NO;
        weakSelf.userPrompt = nil;
        weakSelf.primaryAction = nil;
    }];
    
    [self.userPrompt addAction:self.primaryAction];
    
    [self showPrompt];
}

// Manejar error con mensaje
-(void)handleErrorWithPromptTitle:(NSString *)title message:(NSString *)message withCompletion:(void(^)(void))completionblock {
    
    self.userPrompt = [UIAlertController alertControllerWithTitle:title message:message preferredStyle:UIAlertControllerStyleAlert];
    
    __weak SFFormularioBaseViewController *weakSelf = self;
    self.primaryAction = [UIAlertAction actionWithTitle:kSFDefaultPrimaryAction style:UIAlertActionStyleDefault handler:^(UIAlertAction * _Nonnull action) {
        weakSelf.promptDisplayed = NO;
        weakSelf.userPrompt = nil;
        weakSelf.primaryAction = nil;
        completionblock();
    }];
    
    [self.userPrompt addAction:self.primaryAction];
    
    [self showPrompt];
}

// Mostrar mensaje con informacion
-(void)userInformationPrompt:(NSString *)message {
    self.userPrompt = [UIAlertController alertControllerWithTitle:@"" message:message preferredStyle:UIAlertControllerStyleAlert];
    
    __weak SFFormularioBaseViewController *weakSelf = self;
    self.primaryAction = [UIAlertAction actionWithTitle:kSFDefaultPrimaryAction style:UIAlertActionStyleDefault handler:^(UIAlertAction * _Nonnull action) {
        weakSelf.promptDisplayed = NO;
        weakSelf.userPrompt = nil;
        weakSelf.primaryAction = nil;
    }];
    
    [self.userPrompt addAction:self.primaryAction];
    
    [self showPrompt];
}

#pragma mark - internal

-(void)showPrompt {
    
    if (self.userPrompt && !self.promptDisplayed)
    {
        __weak SFFormularioBaseViewController *weakSelf = self;
        [self presentViewController:self.userPrompt animated:YES completion:^{
            weakSelf.promptDisplayed = YES;
        }];
    }
}

@end
