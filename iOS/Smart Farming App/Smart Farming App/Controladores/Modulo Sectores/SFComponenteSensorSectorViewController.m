//
//  SFComponenteSensorSectorViewController.m
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/30/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFComponenteSensorSectorViewController.h"

#import "ServiciosModuloSectores.h"

@interface SFComponenteSensorSectorViewController ()

@property (strong, nonatomic) IBOutlet UILabel *idComponenteLabel;
@property (strong, nonatomic) IBOutlet UILabel *modeloComponenteLabel;
@property (strong, nonatomic) IBOutlet UILabel *descripcionComponenteLabel;
@property (strong, nonatomic) IBOutlet UILabel *estadoComponenteLabel;
@property (strong, nonatomic) IBOutlet UILabel *cantidadSensoresAsignadosLabel;
@property (strong, nonatomic) IBOutlet UILabel *cantidadMaximaSensoresLabel;

@end

@implementation SFComponenteSensorSectorViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view.
    
    [self obtenerDatos];
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

#pragma mark - Servicio

-(void) obtenerDatos {
    __weak typeof(self) weakSelf = self;
    
    SolcitudMostrarComponenteSensorSector *solicitud = [SolcitudMostrarComponenteSensorSector new];
    solicitud.idFinca = [[ContextoUsuario instance] fincaSeleccionada];
    solicitud.idSector = self.idSector;
    
    [ServiciosModuloSectores mostrarComponenteSensorSector:solicitud completionBlock:^(RespuestaServicioBase *respuesta) {
        [weakSelf hideActivityIndicator];
        
        if ([respuesta isKindOfClass:[RespuestaMostrarComponenteSensorSector class]]) {
            RespuestaMostrarComponenteSensorSector *respuestaMostrarComponenteSensorSector = (RespuestaMostrarComponenteSensorSector *)respuesta;
            
            if (respuestaMostrarComponenteSensorSector.resultado) {
                
                self.idComponenteLabel.text = [NSString stringWithFormat:@"%li", respuestaMostrarComponenteSensorSector.componenteSensor.idComponenteSensor];
                self.modeloComponenteLabel.text = respuestaMostrarComponenteSensorSector.componenteSensor.modelo;
                self.descripcionComponenteLabel.text = respuestaMostrarComponenteSensorSector.componenteSensor.descripcion;
                self.estadoComponenteLabel.text = respuestaMostrarComponenteSensorSector.componenteSensor.estadoComponenteSensor;
                self.cantidadSensoresAsignadosLabel.text = [NSString stringWithFormat:@"%li", respuestaMostrarComponenteSensorSector.componenteSensor.cantidadSensoresAsignados];
                self.cantidadMaximaSensoresLabel.text = [NSString stringWithFormat:@"%li", respuestaMostrarComponenteSensorSector.componenteSensor.cantidadMaximaSensores];
                
            } else {
                [weakSelf handleErrorWithPromptTitle:@"Error obteniendo componente" message:kErrorDesconocido withCompletion:^{
                }];
            }
        }
    } failureBlock:^(ErrorServicioBase *error) {
        [weakSelf hideActivityIndicator];
        [weakSelf handleErrorWithPromptTitle:@"Error obteniendo componente" message:error.detalleError withCompletion:^{
        }];
    }];
}

@end
