//
//  SFFincasEncargadoViewController.m
//  Smart Farming App
//
//  Created by Facundo Palma on 10/14/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFFincasEncargadoViewController.h"

#import "ServiciosModuloFinca.h"

#import "SFFincaTableViewCell.h"

@interface SFFincasEncargadoViewController ()

@property (weak, nonatomic) IBOutlet UITableView *fincasEncargadoTableView;
@property (weak, nonatomic) IBOutlet UILabel *emptyFincasTVMessage;

@end

@implementation SFFincasEncargadoViewController

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
    [self obtenerFincas];
}

-(void)obtenerFincas {
    __weak typeof(self) weakSelf = self;
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
}

#pragma mark - Acciones

-(void)refreshAction {
    [self obtenerFincas];
}

#pragma mark - Configurar vistas

-(void)configurarTabla {
    
    self.tableView = self.fincasEncargadoTableView;
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
