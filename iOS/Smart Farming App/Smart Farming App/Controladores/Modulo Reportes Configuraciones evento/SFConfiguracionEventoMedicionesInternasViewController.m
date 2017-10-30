//
//  SFConfiguracionEventoMedicionesInternasViewController.m
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/30/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFConfiguracionEventoMedicionesInternasViewController.h"

#import "SFConfiguracionEventoMedicionesTabBarViewController.h"

#import "SFMedicionFuenteInterna.h"

@interface SFConfiguracionEventoMedicionesInternasViewController ()

@property (strong, nonatomic) IBOutlet UITableView *medicionesInternaTable;
@property (strong, nonatomic) IBOutlet UILabel *emptyMedicionesInternasLabel;

@end

@implementation SFConfiguracionEventoMedicionesInternasViewController

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

    SFConfiguracionEventoMedicionesTabBarViewController *tabBar = (SFConfiguracionEventoMedicionesTabBarViewController*)self.tabBarController;
    
    self.tableViewItemsArray = tabBar.listaMedicionesInternas;
}

#pragma mark - Acciones

-(void)refreshAction {
    [self obtenerDatosTabla];
}

#pragma mark - Configurar vistas

-(void)configurarTabla {
    
    self.tableView = self.medicionesInternaTable;
    self.emptyTableViewMessageLabel = self.emptyMedicionesInternasLabel;
    
    self.tableView.delegate = self;
    self.tableView.dataSource = self;
    
    [super configurarTabla];
}

#pragma mark - Table view data source/delegate

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
    
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:kTableViewCellIdentifier forIndexPath:indexPath];
 
    SFMedicionFuenteInterna *medicionFuenteInterna = (SFMedicionFuenteInterna*)self.tableViewItemsArray[indexPath.row];
        
    cell.textLabel.text = [NSString stringWithFormat:@"Medición: %@. Unidad: %@", medicionFuenteInterna.nombreTipoMedicion, medicionFuenteInterna.unidadMedicion];
    cell.detailTextLabel.text = [NSString stringWithFormat:@"Valor mínimo: %f, valor máximo: %f", medicionFuenteInterna.valorMinimo, medicionFuenteInterna.valorMaximo];
    
    return cell;
}

@end
