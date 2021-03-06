//
//  SFReporteHeladasOcurrenciasViewController.m
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/31/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFReporteHeladasOcurrenciasViewController.h"

#import "ServiciosModuloReportes.h"

#import "SFOcurrenciaEventoPersonalizado.h"

@interface SFReporteHeladasOcurrenciasViewController ()

@property (strong, nonatomic) IBOutlet UITableView *heladasTableView;
@property (strong, nonatomic) IBOutlet UILabel *emptyEventosLabel;

@end

@implementation SFReporteHeladasOcurrenciasViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view.
    
    [self configurarTabla];
    [self cargaInicialDatos];
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

#pragma mark - Navigation

// In a storyboard-based application, you will often want to do a little preparation before navigation
//- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender {
//    // Get the new view controller using [segue destinationViewController].
//    // Pass the selected object to the new view controller.
//
//    if ([[segue identifier] isEqualToString:kSFNavegarAReporteEventosPersonalizadosRegistradosSegue])
//    {
//        // Get reference to the destination view controller
//        SFReporteEventosPersonalizadosRegistradosViewController *vc = [segue destinationViewController];
//
//        // Pass any objects to the view controller here, like...
//        vc.configuracionEvento = self.configuracionEvento;
//        vc.sector = self.sector;
//    }
//}

#pragma mark - obtener datos

-(void)cargaInicialDatos {
    [self showActivityIndicator];
    [self obtenerDatosTabla];
}

-(void)obtenerDatosTabla {
    __weak typeof(self) weakSelf = self;
    
    SolicitudObtenerInformeHistoricoHeladas *solicitud = [SolicitudObtenerInformeHistoricoHeladas new];
    solicitud.idFinca = [[ContextoUsuario instance] fincaSeleccionada];
    solicitud.idSector = self.idSector;
    solicitud.fechaInicioSector = self.fechaInicioSector;
    solicitud.fechaFinSector = self.fechaFinSector;
    
    [ServiciosModuloReportes obtenerInformeHistoricoHeladas:solicitud completionBlock:^(RespuestaServicioBase *respuesta) {
        [weakSelf hideActivityIndicator];
        
        if ([respuesta isKindOfClass:[RespuestaObtenerInformeHistoricoHeladas class]]) {
            RespuestaObtenerInformeHistoricoHeladas *respuestaObtenerInformeHistoricoHeladas = (RespuestaObtenerInformeHistoricoHeladas *)respuesta;
            
            if (respuestaObtenerInformeHistoricoHeladas.resultado) {
                weakSelf.tableViewItemsArray = respuestaObtenerInformeHistoricoHeladas.listaOcurrenciasHelada;
                [weakSelf loadingTableViewDataDidEnd];
            } else {
                [weakSelf loadingTableViewDataFailed];
                [weakSelf handleErrorWithPromptTitle:@"Error obteniendo eventos" message:kErrorDesconocido withCompletion:^{
                }];
            }
        }
    } failureBlock:^(ErrorServicioBase *error) {
        [weakSelf hideActivityIndicator];
        [weakSelf handleErrorWithPromptTitle:@"Error obteniendo eventos" message:error.detalleError withCompletion:^{
            [weakSelf loadingTableViewDataFailed];
        }];
    }];

}

#pragma mark - Acciones

-(void)refreshAction {
    [self obtenerDatosTabla];
}

#pragma mark - Configurar vistas

-(void)configurarTabla {
    
    self.tableView = self.heladasTableView;
    self.emptyTableViewMessageLabel = self.emptyEventosLabel;
    
    self.tableView.delegate = self;
    self.tableView.dataSource = self;
    
    [super configurarTabla];
}

#pragma mark - Table view data source/delegate

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
    
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:kTableViewCellIdentifier forIndexPath:indexPath];
    
    SFOcurrenciaEventoPersonalizado *evento = (SFOcurrenciaEventoPersonalizado*)self.tableViewItemsArray[indexPath.row];
    
    cell.textLabel.text = [NSString stringWithFormat:@"Número evento: %li - Sector: %li", evento.nroEvento, evento.numeroSector];
    cell.detailTextLabel.text = [NSString stringWithFormat:@"Fecha y hora: %@", [SFUtils formatDateDDMMYYYYTime:evento.fechaYHora]];;
    
    return cell;
}

@end
