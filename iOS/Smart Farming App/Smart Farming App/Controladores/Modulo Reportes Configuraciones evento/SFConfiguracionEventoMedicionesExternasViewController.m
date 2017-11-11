//
//  SFConfiguracionEventoMedicionesExternasViewController.m
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/30/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFConfiguracionEventoMedicionesExternasViewController.h"

#import "SFConfiguracionEventoMedicionesTabBarViewController.h"

#import "SFMedicionFuenteExterna.h"

@interface SFConfiguracionEventoMedicionesExternasViewController ()

@property (strong, nonatomic) IBOutlet UITableView *configuracionesExternasTable;
@property (strong, nonatomic) IBOutlet UILabel *emptyConfiguracionesExternasLabel;

@end

@implementation SFConfiguracionEventoMedicionesExternasViewController

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
    
    self.tableViewItemsArray = tabBar.listaMedicionesExternas;
    [self loadingTableViewDataDidEnd];
}

#pragma mark - Acciones

-(void)refreshAction {
    [self obtenerDatosTabla];
}

#pragma mark - Configurar vistas

-(void)configurarTabla {
    
    self.tableView = self.configuracionesExternasTable;
    self.emptyTableViewMessageLabel = self.emptyConfiguracionesExternasLabel;
    
    self.tableView.delegate = self;
    self.tableView.dataSource = self;
    
    [super configurarTabla];
}

#pragma mark - Table view data source/delegate

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
    
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:kTableViewCellIdentifier forIndexPath:indexPath];
    
    SFMedicionFuenteExterna *medicionFuenteExterna = (SFMedicionFuenteExterna*)self.tableViewItemsArray[indexPath.row];
    
    cell.textLabel.text = [NSString stringWithFormat:@"Medición: %@", medicionFuenteExterna.nombreTipoMedicion];
    cell.detailTextLabel.text = [NSString stringWithFormat:@"Valor (%@) mínimo: %.0f, valor máximo: %.0f",medicionFuenteExterna.unidadMedicion, medicionFuenteExterna.valorMinimo, medicionFuenteExterna.valorMaximo];
    
    return cell;
}

@end
