//
//  SFProveedorInformacionClimaticaViewController.m
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/27/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFProveedorInformacionClimaticaViewController.h"

#import "ServiciosModuloFinca.h"

@interface SFProveedorInformacionClimaticaViewController ()

@property (strong, nonatomic) IBOutlet UILabel *nombreProveedorLabel;
@property (strong, nonatomic) IBOutlet UILabel *urlLabel;
@property (strong, nonatomic) IBOutlet UILabel *frecuenciaElegidaLabel;
@property (strong, nonatomic) IBOutlet UILabel *frecuenciaMaximaLabel;

@property (strong, nonatomic) IBOutlet UITableView *tipoMedicionTableView;
@property (strong, nonatomic) IBOutlet UILabel *sinTipoMedicionLabel;


@end

@implementation SFProveedorInformacionClimaticaViewController

-(void)viewDidLoad {
    [super viewDidLoad];
    
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
    [self obtenerDatosProveedor];
}

-(void)obtenerDatosProveedor {
    __weak typeof(self) weakSelf = self;
    
    SolicitudObtenerProveedorFinca *solicitud = [SolicitudObtenerProveedorFinca new];
    solicitud.idFinca = [[ContextoUsuario instance] fincaSeleccionada];
    
    [self showActivityIndicator];
    [ServiciosModuloFinca obtenerProveedorFinca:solicitud completionBlock:^(RespuestaServicioBase *respuesta) {
        [weakSelf hideActivityIndicator];
        
        if ([respuesta isKindOfClass:[RespuestaObtenerProveedorFinca class]]) {
            RespuestaObtenerProveedorFinca *respuestaObtenerProveedorFinca = (RespuestaObtenerProveedorFinca *)respuesta;
            
            if (respuestaObtenerProveedorFinca.resultado) {
                
                
                
                weakSelf.tableViewItemsArray = respuestaObtenerProveedorFinca.proveedorInformacionClimatica.listaTipoMedicion;
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
    [self obtenerDatosProveedor];
}

#pragma mark - Configurar vistas

-(void)configurarTabla {
    
    self.tableView = self.tipoMedicionTableView;
    self.emptyTableViewMessageLabel = self.sinTipoMedicionLabel;
    
    self.tableView.delegate = self;
    self.tableView.dataSource = self;
    
    [super configurarTabla];
}

#pragma mark - Table view data source/delegate

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
    
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:kTableViewCellIdentifier forIndexPath:indexPath];
    
    SFTipoMedicionClimatica *tipoMedicion = self.tableViewItemsArray[indexPath.row];
    cell.textLabel.text = tipoMedicion.nombreTipoMedicionClimatica;
    cell.detailTextLabel.text = tipoMedicion.unidadMedicion;
    
    return cell;
}

@end
