//
//  SFFincasPendientesViewController.m
//  Smart Farming App
//
//  Created by Facundo Palma on 10/15/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFFincasPendientesViewController.h"
#import "ServiciosModuloFinca.h"

@interface SFFincasPendientesViewController ()

@property (weak, nonatomic) IBOutlet UITableView *fincasPendientesTableView;
@property (weak, nonatomic) IBOutlet UILabel *emptyFincasTVMessage;

@end

@implementation SFFincasPendientesViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    
    [self configurarTabla];
}

-(void)viewWillAppear:(BOOL)animated{
    [super viewWillAppear:animated];
    
    [self obtenerFincas];
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

-(void)obtenerFincas {
    
    
    
//    [ServiciosModuloFinca mostrarFincasEncargadoWithCompletionBlock:^(RespuestaServicioBase *respuesta) {
//        
//        if ([respuesta isKindOfClass:[RespuestaMostrarFincas class]]) {
//            
//            RespuestaMostrarFincas *respuestaMostrarFincas = (RespuestaMostrarFincas *)respuesta;
//            
//            if (respuestaMostrarFincas.resultado) {
//                self.fincas = respuestaMostrarFincas.fincas;
//                [self.tableView reloadData];
//            }
//        }
//    } failureBlock:^(ErrorServicioBase *error) {
//        [self handleErrorWithPromptTitle:@"Error obteniendo fincas" message: error.detalleError];
//    }];
}

#pragma mark - Configurar vistas

-(void)configurarTabla {
   
    self.tableView = self.fincasPendientesTableView;
    self.emptyTableViewMessageLabel = self.emptyFincasTVMessage;
    
    self.tableView.delegate = self;
    self.tableView.dataSource = self;
    
    [super configurarTabla];
}

#pragma mark - Table view data source/delegate

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
    
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:kTableViewCellIdentifier forIndexPath:indexPath];
    
    SFFinca *finca = self.tableViewItemsArray[indexPath.row];
    cell.textLabel.text = finca.nombre;
    
    return cell;
}

@end
