//
//  SFCriteriosInicialesViewController.m
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/30/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFCriteriosInicialesViewController.h"

#import "ServiciosModuloRiego.h"

#import "SFCriteriosRiegoTabBarViewController.h"
#import "SFCriterioConfiguracionRiego.h"
#import "SFCriterioConfiguracionRiegoMedicion.h"
#import "SFCriterioConfiguracionRiegoHora.h"
#import "SFCriterioConfiguracionRiegoVolumenAgua.h"

@interface SFCriteriosInicialesViewController ()

@property (strong, nonatomic) IBOutlet UITableView *criteriosTable;
@property (strong, nonatomic) IBOutlet UILabel *emptyCriteriosLabel;

@end

@implementation SFCriteriosInicialesViewController

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
    
    SolicitudObtenerCriteriosInicialesConfiguracionRiegoMecanismoRiegoFincaSector *solicitud = [SolicitudObtenerCriteriosInicialesConfiguracionRiegoMecanismoRiegoFincaSector new];
    solicitud.idFinca = [[ContextoUsuario instance] fincaSeleccionada];
    solicitud.idMecanismoRiegoFincaSector = tabBar.idMecanismoRiegoSector;
    solicitud.idConfiguracionRiego = tabBar.idConfiguracionRiego;
    
    [ServiciosModuloRiego obtenerCriteriosInicialesConfiguracionRiegoMecanismoRiegoFincaSector:solicitud completionBlock:^(RespuestaServicioBase *respuesta) {
        
        [weakSelf hideActivityIndicator];
        
        if ([respuesta isKindOfClass:[RespuestaObtenerCriteriosInicialesConfiguracionRiegoMecanismoRiegoFincaSector class]]) {
            RespuestaObtenerCriteriosInicialesConfiguracionRiegoMecanismoRiegoFincaSector *respuestaObtenerCriteriosInicialesConfiguracionRiegoMecanismoRiegoFincaSector = (RespuestaObtenerCriteriosInicialesConfiguracionRiegoMecanismoRiegoFincaSector *)respuesta;
            
            if (respuestaObtenerCriteriosInicialesConfiguracionRiegoMecanismoRiegoFincaSector.resultado) {
                weakSelf.tableViewItemsArray = respuestaObtenerCriteriosInicialesConfiguracionRiegoMecanismoRiegoFincaSector.criteriosInicialesConfiguracionRiego;
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
        
        cell.textLabel.text = [NSString stringWithFormat:@"Criterio por medición: %@", criterio.nombreCriterioRiego];
        cell.detailTextLabel.text = [NSString stringWithFormat:@"%@: %@ a %.0f (%@)", criterio.nombreTipoMedicion, criterio.operador, criterio.valor, criterio.unidadMedicion];
    } else if ([self.tableViewItemsArray[indexPath.row] isKindOfClass:[SFCriterioConfiguracionRiegoHora class]]) {
        SFCriterioConfiguracionRiegoHora *criterio = self.tableViewItemsArray[indexPath.row];
        
        cell.textLabel.text = [NSString stringWithFormat:@"Criterio por hora: %@", criterio.nombreCriterioRiego];
        cell.detailTextLabel.text = [NSString stringWithFormat:@"Día %ld, hora: %@", criterio.numeroDia, criterio.hora];
    } else if ([self.tableViewItemsArray[indexPath.row] isKindOfClass:[SFCriterioConfiguracionRiegoVolumenAgua class]]) {
        SFCriterioConfiguracionRiegoVolumenAgua *criterio = self.tableViewItemsArray[indexPath.row];
        
        cell.textLabel.text = [NSString stringWithFormat:@"Criterio por volumen: %@", criterio.nombreCriterioRiego];
        cell.detailTextLabel.text = [NSString stringWithFormat:@"Volumen (lts): %.2f", criterio.volumen];
    }
    return cell;
}

@end
