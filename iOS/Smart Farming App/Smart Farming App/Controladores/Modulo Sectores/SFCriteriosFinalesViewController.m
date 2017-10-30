//
//  SFCriteriosFinalesViewController.m
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/30/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFCriteriosFinalesViewController.h"

#import "ServiciosModuloRiego.h"

#import "SFCriteriosRiegoTabBarViewController.h"
#import "SFCriterioConfiguracionRiego.h"
#import "SFCriterioConfiguracionRiegoMedicion.h"
#import "SFCriterioConfiguracionRiegoHora.h"
#import "SFCriterioConfiguracionRiegoVolumenAgua.h"

@interface SFCriteriosFinalesViewController ()

@property (strong, nonatomic) IBOutlet UITableView *criteriosTable;
@property (strong, nonatomic) IBOutlet UILabel *emptyCriteriosLabel;

@end

@implementation SFCriteriosFinalesViewController

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
}

#pragma mark - obtener datos

-(void)cargaInicialDatos {
    [self showActivityIndicator];
    [self obtenerDatosTabla];
}

-(void)obtenerDatosTabla {
    __weak typeof(self) weakSelf = self;
    
    SFCriteriosRiegoTabBarViewController *tabBar = (SFCriteriosRiegoTabBarViewController*)self.tabBarController;
    
    SolicitudObtenerCriteriosFinalesConfiguracionRiegoMecanismoRiegoFincaSector *solicitud = [SolicitudObtenerCriteriosFinalesConfiguracionRiegoMecanismoRiegoFincaSector new];
    solicitud.idFinca = [[ContextoUsuario instance] fincaSeleccionada];
    solicitud.idMecanismoRiegoFincaSector = tabBar.idConfiguracionRiego;
    solicitud.idConfiguracionRiego = tabBar.idConfiguracionRiego;
    
    [ServiciosModuloRiego obtenerCriteriosFinalesConfiguracionRiegoMecanismoRiegoFincaSector:solicitud completionBlock:^(RespuestaServicioBase *respuesta) {
        [weakSelf hideActivityIndicator];
        
        if ([respuesta isKindOfClass:[RespuestaObtenerCriteriosFinalesConfiguracionRiegoMecanismoRiegoFincaSector class]]) {
            RespuestaObtenerCriteriosFinalesConfiguracionRiegoMecanismoRiegoFincaSector *respuestaObtenerCriteriosIFinalesConfiguracionRiegoMecanismoRiegoFincaSector = (RespuestaObtenerCriteriosFinalesConfiguracionRiegoMecanismoRiegoFincaSector *)respuesta;
            
            if (respuestaObtenerCriteriosIFinalesConfiguracionRiegoMecanismoRiegoFincaSector.resultado) {
                weakSelf.tableViewItemsArray = respuestaObtenerCriteriosIFinalesConfiguracionRiegoMecanismoRiegoFincaSector.criteriosFinalesConfiguracionRiego;
                [weakSelf loadingTableViewDataDidEnd];
            } else {
                [weakSelf loadingTableViewDataFailed];
                [weakSelf handleErrorWithPromptTitle:@"Error obteniendo criterios" message:kErrorDesconocido withCompletion:^{
                }];
            }
        }
    } failureBlock:^(ErrorServicioBase *error) {
        [weakSelf hideActivityIndicator];
        [weakSelf handleErrorWithPromptTitle:@"Error obteniendo criterios" message:error.detalleError withCompletion:^{
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
    
    self.tableView = self.criteriosTable;
    self.emptyTableViewMessageLabel = self.emptyCriteriosLabel;
    
    self.tableView.delegate = self;
    self.tableView.dataSource = self;
    
    [super configurarTabla];
}

#pragma mark - Table view data source/delegate

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
    
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:kTableViewCellIdentifier forIndexPath:indexPath];
    
    if ([self.tableViewItemsArray[indexPath.row] isKindOfClass:[SFCriterioConfiguracionRiegoMedicion class]]) {
        SFCriterioConfiguracionRiegoMedicion *criterio = self.tableViewItemsArray[indexPath.row];
        
        cell.textLabel.text = [NSString stringWithFormat:@"Criterio por medición: %@. Tipo medición: %@", criterio.nombreCriterioRiego, criterio.nombreTipoMedicion];
        cell.detailTextLabel.text = [NSString stringWithFormat:@"Valor %@: %f", criterio.operador, criterio.valor];
    } else if ([self.tableViewItemsArray[indexPath.row] isKindOfClass:[SFCriterioConfiguracionRiegoHora class]]) {
        SFCriterioConfiguracionRiegoHora *criterio = self.tableViewItemsArray[indexPath.row];
        
        cell.textLabel.text = [NSString stringWithFormat:@"Criterio por hora: %@", criterio.nombreCriterioRiego];
        cell.detailTextLabel.text = [NSString stringWithFormat:@"Día %ld, hora: %@", criterio.numeroDia, criterio.hora];
    } else if ([self.tableViewItemsArray[indexPath.row] isKindOfClass:[SFCriterioConfiguracionRiegoVolumenAgua class]]) {
        SFCriterioConfiguracionRiegoVolumenAgua *criterio = self.tableViewItemsArray[indexPath.row];
        
        cell.textLabel.text = [NSString stringWithFormat:@"Criterio por volumen: %@", criterio.nombreCriterioRiego];
        cell.detailTextLabel.text = [NSString stringWithFormat:@"Volumen (lts): %@", criterio.volumen];
    }
    return cell;
}


@end
