//
//  SFConfiguracionesRiegoViewController.m
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/30/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFConfiguracionesRiegoViewController.h"

#import "SFConfiguracionRiego.h"
#import "SFCriteriosRiegoTabBarViewController.h"
#import "ServiciosModuloRiego.h"

@interface SFConfiguracionesRiegoViewController ()

@property (strong, nonatomic) IBOutlet UITableView *configuracionesRiegoTable;
@property (strong, nonatomic) IBOutlet UILabel *emptyConfiguracionesLabel;

@property (strong, nonatomic) SFConfiguracionRiego *configuracionRiego;

@end

@implementation SFConfiguracionesRiegoViewController

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
    
    if ([[segue identifier] isEqualToString:kSFNavegarAInfoSectorSegue])
    {
        // Get reference to the destination view controller
        SFCriteriosRiegoTabBarViewController *vc = [segue destinationViewController];
        
        // Pass any objects to the view controller here, like...
        vc.idSector = self.idSector;
        vc.idMecanismoRiegoSector = self.idMecanismoRiegoSector;
        vc.idConfiguracionRiego = self.configuracionRiego.idConfiguracionRiego;
    }
}

#pragma mark - obtener datos

-(void)cargaInicialDatos {
    [self showActivityIndicator];
    [self obtenerDatosTabla];
}

-(void)obtenerDatosTabla {
    __weak typeof(self) weakSelf = self;
    
    SolicitudObtenerConfiguracionesRiegoMecanismoRiegoFincaSector *solicitud = [SolicitudObtenerConfiguracionesRiegoMecanismoRiegoFincaSector new];
    solicitud.idFinca = [[ContextoUsuario instance] fincaSeleccionada];
    solicitud.idMecanismoRiegoFincaSector = self.idMecanismoRiegoSector;
    
    [ServiciosModuloRiego obtenerConfiguracionesRiegoMecanismoRiegoFincaSector:solicitud completionBlock:^(RespuestaServicioBase *respuesta) {
        [weakSelf hideActivityIndicator];
        
        if ([respuesta isKindOfClass:[RespuestaObtenerConfiguracionesRiegoMecanismoRiegoFincaSector class]]) {
            RespuestaObtenerConfiguracionesRiegoMecanismoRiegoFincaSector *respuestaObtenerConfiguracionesRiegoMecanismoRiegoFincaSector = (RespuestaObtenerConfiguracionesRiegoMecanismoRiegoFincaSector *)respuesta;
            
            if (respuestaObtenerConfiguracionesRiegoMecanismoRiegoFincaSector.resultado) {
                weakSelf.tableViewItemsArray = respuestaObtenerConfiguracionesRiegoMecanismoRiegoFincaSector.configuracionesRiego;
                [weakSelf loadingTableViewDataDidEnd];
            } else {
                [weakSelf loadingTableViewDataFailed];
                [weakSelf handleErrorWithPromptTitle:@"Error obteniendo configuraciones" message:kErrorDesconocido withCompletion:^{
                }];
            }
        }
    } failureBlock:^(ErrorServicioBase *error) {
        [weakSelf hideActivityIndicator];
        [weakSelf handleErrorWithPromptTitle:@"Error obteniendo configuraciones" message:error.detalleError withCompletion:^{
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
    
    self.tableView = self.configuracionesRiegoTable;
    self.emptyTableViewMessageLabel = self.emptyConfiguracionesLabel;
    
    self.tableView.delegate = self;
    self.tableView.dataSource = self;
    
    [super configurarTabla];
}

#pragma mark - Table view data source/delegate

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
    
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:kTableViewCellIdentifier forIndexPath:indexPath];
    
    SFConfiguracionRiego *configuracion = self.tableViewItemsArray[indexPath.row];
    cell.textLabel.text = configuracion.nombreConfiguracionRiego;
    cell.detailTextLabel.text = configuracion.nombreTipoConfiguracionRiego;
    
    return cell;
}

-(void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath {
    
    self.configuracionRiego = self.tableViewItemsArray[indexPath.row];
    
    if ([self.configuracionRiego.nombreTipoConfiguracionRiego isEqualToString:@"automatico"]) {
        [self userInformationPrompt:@"Las configuraciones automáticas no tienen criterios"];
    }
    else{
        [self performSegueWithIdentifier:kSFNavegarCriteriosRiegoSegue sender:self];
    }
}

@end
