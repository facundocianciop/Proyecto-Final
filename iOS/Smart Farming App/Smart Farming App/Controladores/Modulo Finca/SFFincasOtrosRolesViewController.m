//
//  SFFincasOtrosRolesViewController.m
//  Smart Farming App
//
//  Created by Facundo Palma on 10/14/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFFincasOtrosRolesViewController.h"
#import "ServiciosModuloFinca.h"

@interface SFFincasOtrosRolesViewController ()

@property (weak, nonatomic) IBOutlet UIPickerView *rolPicker;
@property (strong, nonatomic) NSArray *rolesArray;

@property (weak, nonatomic) IBOutlet UITableView *otrosRolesFincasTableView;
@property (weak, nonatomic) IBOutlet UILabel *emptyFincasTVMessage;

@end

@implementation SFFincasOtrosRolesViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    
    // Configurar vistas
    [self configurarPicker];
    [self configurarTabla];
}

-(void)viewWillAppear:(BOOL)animated {
    [super viewWillAppear:animated];
    
    self.rolesArray = [self obtenerRoles];
    self.tableViewItemsArray = [self obtenerFincas];
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

/*
#pragma mark - Navigation

// In a storyboard-based application, you will often want to do a little preparation before navigation
- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender {
    // Get the new view controller using [segue destinationViewController].
    // Pass the selected object to the new view controller.
}
*/

#pragma mark - obtener datos

-(NSArray *)obtenerRoles {
    
    NSMutableArray *roles = [NSMutableArray arrayWithObjects:@"Stakeholder",@"Otro Rol",nil];
 
    return roles;
}

-(NSArray *)obtenerFincas {
    
    NSMutableArray *fincas = [NSMutableArray new];
    
    return fincas;
}

#pragma mark - Configurar vistas

-(void)configurarPicker {
    self.rolPicker.delegate = self;
    self.rolPicker.dataSource = self;
}

-(void)configurarTabla {
    
    self.tableView = self.otrosRolesFincasTableView;
    self.emptyTableViewMessageLabel = self.emptyFincasTVMessage;
    
    self.tableView.delegate = self;
    self.tableView.dataSource = self;
    
    [super configurarTabla];
}

#pragma mark - Picker Configutation

- (NSInteger)numberOfComponentsInPickerView:(nonnull UIPickerView *)pickerView {
    return 1;
}

- (NSInteger)pickerView:(nonnull UIPickerView *)pickerView numberOfRowsInComponent:(NSInteger)component {
    return [self.rolesArray count];
}

-(NSString *)pickerView:(UIPickerView *)pickerView titleForRow:(NSInteger)row forComponent:(NSInteger)component {
    return self.rolesArray[row];
}

- (void)didUpdateFocusInContext:(nonnull UIFocusUpdateContext *)context withAnimationCoordinator:(nonnull UIFocusAnimationCoordinator *)coordinator {
    
}

#pragma mark - Table View Configuration


- (nonnull UITableViewCell *)tableView:(nonnull UITableView *)tableView cellForRowAtIndexPath:(nonnull NSIndexPath *)indexPath {
    UITableViewCell *cell = [UITableViewCell new];
    
    return cell;
}

@end
