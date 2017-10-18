//
//  SFMecanismosRiegoHabilitadosViewController.m
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/18/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFMecanismosRiegoHabilitadosViewController.h"

#import "SFMecanismoRiegoFincaSector.h"

@interface SFMecanismosRiegoHabilitadosViewController ()

@property (strong, nonatomic) IBOutlet UILabel *emptyMecanismosRiegoLabel;
@property (strong, nonatomic) IBOutlet UITableView *mecanismosRiegoHabilitadosTableView;

@end

@implementation SFMecanismosRiegoHabilitadosViewController

-(void)viewDidLoad {
    [super viewDidLoad];
    
    [self configurarTabla];
    
    [self cargaInicialDatos];
}

-(void)didReceiveMemoryWarning {
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
    [self obtenerMecanismoRiegoFincaSector];
}

-(void)obtenerMecanismoRiegoFincaSector {
    __weak typeof(self) weakSelf = self;
    /*
     [ServiciosModuloFinca mostrarFincasEncargadoWithCompletionBlock:^(RespuestaServicioBase *respuesta) {
     [weakSelf hideActivityIndicator];
     
     if ([respuesta isKindOfClass:[RespuestaMostrarFincas class]]) {
     RespuestaMostrarFincas *respuestaMostrarFincas = (RespuestaMostrarFincas *)respuesta;
     
     if (respuestaMostrarFincas.resultado) {
     weakSelf.tableViewItemsArray = respuestaMostrarFincas.fincas;
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
     */
}

#pragma mark - Acciones

-(void)refreshAction {
    [self obtenerMecanismoRiegoFincaSector];
}

#pragma mark - Configurar vistas

-(void)configurarTabla {
    
    self.tableView = self.mecanismosRiegoHabilitadosTableView;
    self.emptyTableViewMessageLabel = self.emptyMecanismosRiegoLabel;
    
    self.tableView.delegate = self;
    self.tableView.dataSource = self;
    
    [super configurarTabla];
}

#pragma mark - Table view data source/delegate

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
    
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:kTableViewCellIdentifier forIndexPath:indexPath];
    
    SFMecanismoRiegoFincaSector *mecanismoRiegoFincaSector = self.tableViewItemsArray[indexPath.row];
    //cell.textLabel.text = mecanismoRiegoFincaSector.nombreSector;
    //cell.detailTextLabel.text = [NSString stringWithFormat:@"Numero sector: %li", mecanismoRiegoFincaSector.numeroSector];
    
    return cell;
}

-(void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath {
    
}

@end
