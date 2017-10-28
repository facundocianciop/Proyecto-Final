//
//  SFFincasOtrosRolesViewController.m
//  Smart Farming App
//
//  Created by Facundo Palma on 10/14/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFFincasOtrosRolesViewController.h"
#import "ServiciosModuloFinca.h"

#import "SFFincaTableViewCell.h"

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
    
    [self cargaInicialDatos];
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

-(void)cargaInicialDatos {
    [self showActivityIndicator];
    [self obtenerRoles];
}

-(void)obtenerRoles {
    __weak typeof(self) weakSelf = self;
    [ServiciosModuloFinca buscarRoles:^(RespuestaServicioBase *respuesta) {
        
        if ([respuesta isKindOfClass:[RespuestaBuscarRoles class]]) {
            [weakSelf hideActivityIndicator];
            
            RespuestaBuscarRoles *respuestaBuscarRoles = (RespuestaBuscarRoles *)respuesta;
            
            if (respuestaBuscarRoles.resultado) {
                NSMutableArray *roles = [NSMutableArray new];
                for (NSString *rol in respuestaBuscarRoles.nombreRoles) {
                    if (![rol isEqualToString:kRolEncargado]) {
                        [roles addObject:rol];
                    }
                }
                weakSelf.rolesArray = roles;
                [weakSelf.rolPicker reloadAllComponents];
                [weakSelf beginTableViewDataLoading];
                [weakSelf obtenerFincas];
            } else {
                [weakSelf handleErrorWithPromptTitle:kErrorObteniendoRoles message:kErrorDesconocido withCompletion:^{
                }];
            }
        }
    } failureBlock:^(ErrorServicioBase *error) {
        [weakSelf hideActivityIndicator];
        [weakSelf handleErrorWithPromptTitle:kErrorObteniendoRoles message:error.detalleError withCompletion:^{
        }];
    }];
}

-(void)obtenerFincas {
    
    __weak typeof(self) weakSelf = self;
    [ServiciosModuloFinca obtenerFincasPorUsuario:^(RespuestaServicioBase *respuesta) {
        if ([respuesta isKindOfClass:[RespuestaMostrarFincas class]]) {
            [weakSelf hideActivityIndicator];
            
            RespuestaMostrarFincas *respuestaMostrarFincas = (RespuestaMostrarFincas *)respuesta;
            
            if (respuestaMostrarFincas.resultado) {
                
                NSString *rolElegido = [weakSelf.rolPicker.delegate pickerView:weakSelf.rolPicker titleForRow:[weakSelf.rolPicker selectedRowInComponent:0] forComponent:0];
                
                NSMutableArray *fincasConRol = [NSMutableArray new];
                for (SFFinca *finca in respuestaMostrarFincas.fincas) {
                    if ([finca.rolUsuario isEqualToString:rolElegido]) {
                        [fincasConRol addObject:finca];
                    }
                }
                weakSelf.tableViewItemsArray = fincasConRol;
                [weakSelf loadingTableViewDataDidEnd];
            } else {
                [weakSelf loadingTableViewDataFailed];
                [weakSelf handleErrorWithPromptTitle:kErrorObteniendoFincas message:kErrorDesconocido withCompletion:^{
                }];
            }
        }
    } failureBlock:^(ErrorServicioBase *error) {
        [weakSelf hideActivityIndicator];
        [weakSelf handleErrorWithPromptTitle:kErrorObteniendoFincas message:error.detalleError withCompletion:^{
            [weakSelf loadingTableViewDataFailed];
        }];
    }];
}

#pragma mark - Acciones

-(void)refreshAction {
    [self obtenerFincas];
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

-(void)pickerView:(UIPickerView *)pickerView didSelectRow:(NSInteger)row inComponent:(NSInteger)component {
    [self beginTableViewDataLoading];
    [self obtenerFincas];
}

#pragma mark - Table View Configuration

- (nonnull UITableViewCell *)tableView:(nonnull UITableView *)tableView cellForRowAtIndexPath:(nonnull NSIndexPath *)indexPath {
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:kTableViewCellIdentifier forIndexPath:indexPath];
    
    SFFinca *finca = self.tableViewItemsArray[indexPath.row];
    cell.textLabel.text = finca.nombre;
    cell.detailTextLabel.text = finca.direccionLegal;
    
    return cell;
}

-(void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath {
    
    SFFinca *finca = self.tableViewItemsArray[indexPath.row];
    
    SolicitudDevolverPermisos *solicitud = [SolicitudDevolverPermisos new];
    solicitud.idFinca = finca.idFinca;
    
    __weak typeof(self) weakSelf = self;
    [ServiciosModuloFinca devolverPermisos:solicitud completionBlock:^(RespuestaServicioBase *respuesta) {
        [weakSelf hideActivityIndicator];
        
        if ([respuesta isKindOfClass:[RespuestaDevolverPermisos class]]) {
            RespuestaDevolverPermisos *respuestaDevolverPermisos = (RespuestaDevolverPermisos *)respuesta;
            
            if (respuestaDevolverPermisos.resultado) {
                
                [[ContextoUsuario instance] seleccionarFinca:finca.idFinca];
                [[ContextoUsuario instance] setPermisosFincaSeleccionada:respuestaDevolverPermisos.conjuntoPermisos];
                
                [self performSegueWithIdentifier:kSFNavegarASeccionFincaSegue sender:self];
            } else {
                [weakSelf handleErrorWithPromptTitle:kErrorObteniendoDatosFinca message:kErrorDesconocido withCompletion:^{
                }];
            }
        }
    } failureBlock:^(ErrorServicioBase *error) {
        [weakSelf hideActivityIndicator];
        [weakSelf handleErrorWithPromptTitle:kErrorObteniendoDatosFinca message:error.detalleError withCompletion:^{
        }];
    }];
}

@end
