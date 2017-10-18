//
//  SFSectoresTableViewController.m
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/18/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFSectoresTableViewController.h"

#import "ServiciosModuloSectores.h"

@interface SFSectoresTableViewController ()


@property (strong, nonatomic) IBOutlet UITableView *sectoresTableView;
@property (strong, nonatomic) IBOutlet UILabel *emptySectoresTVMessage;

@end

@implementation SFSectoresTableViewController

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
    [self obtenerSectores];
}

-(void)obtenerSectores {
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
    [self obtenerSectores];
}

#pragma mark - Configurar vistas

-(void)configurarTabla {
    
    self.tableView = self.sectoresTableView;
    self.emptyTableViewMessageLabel = self.emptySectoresTVMessage;
    
    self.tableView.delegate = self;
    self.tableView.dataSource = self;
    
    [super configurarTabla];
}

#pragma mark - Table view data source/delegate

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
    
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:kTableViewCellIdentifier forIndexPath:indexPath];
    
    SFSectorFinca *sector = self.tableViewItemsArray[indexPath.row];
    cell.textLabel.text = sector.nombreSector;
    cell.detailTextLabel.text = [NSString stringWithFormat:@"Numero sector: %li", sector.numeroSector];
    
    return cell;
}

-(void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath {
    
    [self performSegueWithIdentifier:kSFNavegarAInfoSectorSegue sender:self];
    
}

@end
