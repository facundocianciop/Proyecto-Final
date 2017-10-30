//
//  SFConfiguracionesEventoViewController.m
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/30/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFConfiguracionesEventoViewController.h"

#import "ServiciosModuloReportes.h"

#import "SFConfiguracionEvento.h"
#import "SFMedicionFuenteInterna.h"
#import "SFMedicionFuenteExterna.h"

#import "SFConfiguracionEventoMedicionesTabBarViewController.h"

@interface SFConfiguracionesEventoViewController ()

@property (strong, nonatomic) IBOutlet UITableView *configuracionesTable;
@property (strong, nonatomic) IBOutlet UILabel *emptyConfiguracionesLabel;

@property (assign, nonatomic) NSArray<SFMedicionFuenteInterna*> *listaMedicionesInternas;
@property (assign, nonatomic) NSArray<SFMedicionFuenteExterna*> *listaMedicionesExternas;

@end

@implementation SFConfiguracionesEventoViewController

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
- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender {
    // Get the new view controller using [segue destinationViewController].
    // Pass the selected object to the new view controller.
    
    if ([[segue identifier] isEqualToString:kSFNavegarAMedicionesConfiguracionEvento])
    {
        // Get reference to the destination view controller
        SFConfiguracionEventoMedicionesTabBarViewController *vc = [segue destinationViewController];
        
        // Pass any objects to the view controller here, like...
        vc.listaMedicionesInternas = self.listaMedicionesInternas;
        vc.listaMedicionesExternas = self.listaMedicionesExternas;
    }
}

#pragma mark - obtener datos

-(void)cargaInicialDatos {
    [self showActivityIndicator];
    [self obtenerDatosTabla];
}

-(void)obtenerDatosTabla {
    __weak typeof(self) weakSelf = self;
    
    SolicitudBuscarConfiguracionesEventosPersonalizados *solicitud = [SolicitudBuscarConfiguracionesEventosPersonalizados new];
    solicitud.idFinca = [[ContextoUsuario instance] fincaSeleccionada];
    solicitud.idUsuarioFinca = [[ContextoUsuario instance] usuarioFincaIdSeleccionado];
    
    [ServiciosModuloReportes buscarConfiguracionesEventosPersonalizados:solicitud completionBlock:^(RespuestaServicioBase *respuesta) {
        [weakSelf hideActivityIndicator];
        
        if ([respuesta isKindOfClass:[RespuestaBuscarConfiguracionesEventosPersonalizados class]]) {
            RespuestaBuscarConfiguracionesEventosPersonalizados *respuestaBuscarConfiguracionesEventosPersonalizados = (RespuestaBuscarConfiguracionesEventosPersonalizados *)respuesta;
            
            if (respuestaBuscarConfiguracionesEventosPersonalizados.resultado) {
                weakSelf.tableViewItemsArray = respuestaBuscarConfiguracionesEventosPersonalizados.configuracionesEvento;
                [weakSelf loadingTableViewDataDidEnd];
            } else {
                [weakSelf loadingTableViewDataFailed];
                [weakSelf handleErrorWithPromptTitle:@"Error obteniendo configuraciones de eventos" message:kErrorDesconocido withCompletion:^{
                }];
            }
        }
    } failureBlock:^(ErrorServicioBase *error) {
        [weakSelf hideActivityIndicator];
        [weakSelf handleErrorWithPromptTitle:@"Error obteniendo configuraciones de eventos" message:error.detalleError withCompletion:^{
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
    
    self.tableView = self.configuracionesTable;
    self.emptyTableViewMessageLabel = self.emptyConfiguracionesLabel;
    
    self.tableView.delegate = self;
    self.tableView.dataSource = self;
    
    [super configurarTabla];
}

#pragma mark - Table view data source/delegate

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
    
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:kTableViewCellIdentifier forIndexPath:indexPath];
    
    SFConfiguracionEvento *configuracion = (SFConfiguracionEvento*)self.tableViewItemsArray[indexPath.row];
    
    cell.textLabel.text = configuracion.nombreConfiguracioEvento;
    cell.detailTextLabel.text = [NSString stringWithFormat:@" %s", configuracion.activado ? "Activado" : "Desactivada"];
    
    return cell;
}

-(void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath {
    
    SFConfiguracionEvento *configuracion = (SFConfiguracionEvento*)self.tableViewItemsArray[indexPath.row];
    
    self.listaMedicionesInternas = configuracion.listaMedicionesInternas;
    self.listaMedicionesExternas = configuracion.listaMedicionesExternas;
 
    [self performSegueWithIdentifier:kSFNavegarAMedicionesConfiguracionEvento sender:self];
}

@end
