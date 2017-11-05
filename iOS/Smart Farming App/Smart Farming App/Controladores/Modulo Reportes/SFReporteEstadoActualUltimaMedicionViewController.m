//
//  SFReporteEstadoActualUltimaMedicionViewController.m
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/31/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFReporteEstadoActualUltimaMedicionViewController.h"

@interface SFReporteEstadoActualUltimaMedicionViewController ()

@property (strong, nonatomic) IBOutlet UITableView *medicionTableView;
@property (strong, nonatomic) IBOutlet UILabel *emptyMedicionesLabel;

@property (strong, nonatomic) IBOutlet UILabel *fechaHoraLabel;

@end

@implementation SFReporteEstadoActualUltimaMedicionViewController

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
    [self obtenerDatosTabla];
}

-(void)obtenerDatosTabla {
    
    if (self.medicion.fechaYHora) {
        self.fechaHoraLabel.text = [SFUtils formatDateDDMMYYYYTime:self.medicion.fechaYHora];
    }
    
    self.tableViewItemsArray = self.medicion.listaDetallesMedicion;
    [self loadingTableViewDataDidEnd];
}

#pragma mark - Acciones

-(void)refreshAction {
    [self obtenerDatosTabla];
}

#pragma mark - Configurar vistas

-(void)configurarTabla {
    
    self.tableView = self.medicionTableView;
    self.emptyTableViewMessageLabel = self.emptyMedicionesLabel;
    
    self.tableView.delegate = self;
    self.tableView.dataSource = self;
    
    [super configurarTabla];
}

#pragma mark - Table view data source/delegate

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
    
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:kTableViewCellIdentifier forIndexPath:indexPath];
    
    SFMedicionSensorDetalle *detalle = self.tableViewItemsArray[indexPath.row];
    
    cell.textLabel.text = [NSString stringWithFormat:@"%li - Medición: %@", detalle.nroRenglon, detalle.nombreTipoMedicion];
    cell.detailTextLabel.text = [NSString stringWithFormat:@"Valor: %.0f", detalle.valorMedicion];
    
    return cell;
}

@end
