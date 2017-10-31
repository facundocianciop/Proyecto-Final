//
//  SFMecanismosRiegoHabilitadosViewController.m
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/18/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFMecanismosRiegoHabilitadosViewController.h"

#import "SFMecanismoRiegoFincaSector.h"
#import "SFDetallesMecanismoRiegoViewController.h"

#import "ServiciosModuloFinca.h"
#import "ServiciosModuloSectores.h"

@interface SFMecanismosRiegoHabilitadosViewController ()

@property (strong, nonatomic) IBOutlet UILabel *emptyMecanismosRiegoLabel;
@property (strong, nonatomic) IBOutlet UITableView *mecanismosRiegoHabilitadosTableView;

@property (strong, nonatomic) NSMutableArray<SFMecanismoRiegoFincaSector*> *listaMecanismosRiego;

@property (strong, nonatomic) SFMecanismoRiegoFincaSector *mecanismoRiego;

@end

@implementation SFMecanismosRiegoHabilitadosViewController

-(void)viewDidLoad {
    [super viewDidLoad];
    
    self.listaMecanismosRiego = [NSMutableArray new];
    [self configurarTabla];
    [self cargaInicialDatos];
}

-(void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

// In a storyboard-based application, you will often want to do a little preparation before navigation
- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender {
    // Get the new view controller using [segue destinationViewController].
    // Pass the selected object to the new view controller.
    
    if ([[segue identifier] isEqualToString:kSFNavegarInfoEjecucionRiego])
    {
        // Get reference to the destination view controller
        SFDetallesMecanismoRiegoViewController *vc = [segue destinationViewController];
        
        // Pass any objects to the view controller here, like...
        vc.mecanismoRiego = self.mecanismoRiego;
    }
}

#pragma mark - obtener datos

-(void)cargaInicialDatos {
    [self showActivityIndicator];
    [self obtenerSectores];
}

-(void)obtenerSectores {
    __weak typeof(self) weakSelf = self;
    
    [self.listaMecanismosRiego removeAllObjects];
    
    SolicitudMostrarSectores *solicitud = [SolicitudMostrarSectores new];
    solicitud.idFinca = [[ContextoUsuario instance] fincaSeleccionada];
    
    [ServiciosModuloSectores mostrarSectores:solicitud completionBlock:^(RespuestaServicioBase *respuesta) {
        [weakSelf hideActivityIndicator];
        if ([respuesta isKindOfClass:[RespuestaMostrarSectores class]]) {
            RespuestaMostrarSectores *respuestaMostrarSectores = (RespuestaMostrarSectores *)respuesta;
            
            if (respuestaMostrarSectores.resultado) {
                weakSelf.tableViewItemsArray = respuestaMostrarSectores.sectores;
                
                for (SFSectorFinca *sector in respuestaMostrarSectores.sectores) {
                    [weakSelf obtenerMecanismoSector:sector.idSector nombreSector:sector.nombreSector];
                }
                
                [weakSelf loadingTableViewDataDidEnd];
            } else {
                [weakSelf loadingTableViewDataFailed];
                [weakSelf handleErrorWithPromptTitle:@"Error obteniendo sectores" message:kErrorDesconocido withCompletion:^{
                }];
            }
        }
        
    } failureBlock:^(ErrorServicioBase *error) {
        [weakSelf hideActivityIndicator];
        [weakSelf handleErrorWithPromptTitle:@"Error obteniendo sectores" message:error.detalleError withCompletion:^{
            [weakSelf loadingTableViewDataFailed];
        }];
    }];
}

-(void)obtenerMecanismoSector:(long)idSector nombreSector:(NSString*)nombreSector{
    
    __block NSString *nombreSector_block = nombreSector;
    __weak typeof(self) weakSelf = self;
    
    SolicitudMostrarMecanismoRiegoSector *solicitud = [SolicitudMostrarMecanismoRiegoSector new];
    solicitud.idFinca = [[ContextoUsuario instance] fincaSeleccionada];
    solicitud.idSector = idSector;

    [ServiciosModuloSectores mostrarMecanismoRiegoSector:solicitud completionBlock:^(RespuestaServicioBase *respuesta) {
        
        if ([respuesta isKindOfClass:[RespuestaMostrarMecanismoRiegoSector class]]) {
            RespuestaMostrarMecanismoRiegoSector *respuestaMostrarMecanismoRiegoSector = (RespuestaMostrarMecanismoRiegoSector *)respuesta;
            
            if (respuestaMostrarMecanismoRiegoSector.resultado) {
                
                respuestaMostrarMecanismoRiegoSector.mecanismoRiegoFincaSector.nombreSector = nombreSector_block;
                [weakSelf.listaMecanismosRiego addObject:respuestaMostrarMecanismoRiegoSector.mecanismoRiegoFincaSector];
                [weakSelf loadingTableViewDataDidEnd];
            } else {
                [weakSelf hideActivityIndicator];
                [weakSelf handleErrorWithPromptTitle:@"Error obteniendo mecanismo" message:kErrorDesconocido withCompletion:^{
                    [weakSelf loadingTableViewDataFailed];
                }];
            }
        }
    } failureBlock:^(ErrorServicioBase *error) {
        [weakSelf hideActivityIndicator];
        [weakSelf handleErrorWithPromptTitle:@"Error obteniendo mecanismo" message:error.detalleError withCompletion:^{
            [weakSelf loadingTableViewDataFailed];
        }];
    }];
}

#pragma mark - Acciones

-(void)refreshAction {
    [self obtenerSectores];
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

-(NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section {
    
    return [self.listaMecanismosRiego count];
}

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
    
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:kTableViewCellIdentifier forIndexPath:indexPath];
    
    SFMecanismoRiegoFincaSector *mecanismoRiegoFincaSector = self.listaMecanismosRiego[indexPath.row];
    cell.textLabel.text = mecanismoRiegoFincaSector.nombreTipoMecanismo;
    cell.detailTextLabel.text = [NSString stringWithFormat:@"Sector: %@", mecanismoRiegoFincaSector.nombreSector];
    
    return cell;
}

-(void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath {
    
    self.mecanismoRiego = self.listaMecanismosRiego[indexPath.row];
    [self performSegueWithIdentifier:kSFNavegarInfoEjecucionRiego sender:self];
}

@end
