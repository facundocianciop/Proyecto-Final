//
//  SFReporteEstadoActualSectorDetalleViewController.m
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/31/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFReporteEstadoActualSectorDetalleViewController.h"

#import "ServiciosModuloReportes.h"

#import "SFReporteEstadoActualEjecucionRiegoViewController.h"
#import "SFReporteEstadoActualUltimaMedicionViewController.h"

@interface SFReporteEstadoActualSectorDetalleViewController ()

@property (strong, nonatomic) IBOutlet UILabel *numSectorLabel;
@property (strong, nonatomic) IBOutlet UILabel *descripcionSectorLabel;
@property (strong, nonatomic) IBOutlet UILabel *superficieLabel;
@property (strong, nonatomic) IBOutlet UILabel *modeloComponenteLabel;
@property (strong, nonatomic) IBOutlet UILabel *estadoComponenteLabel;
@property (strong, nonatomic) IBOutlet UILabel *tipoMecanismoLabel;

@property (strong, nonatomic) SFMedicionSensorCabecera *medicion;
@property (strong, nonatomic) SFEjecucionRiego *ejecucion;

@end

@implementation SFReporteEstadoActualSectorDetalleViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view.
    
    [self obtenerDatos];
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

// In a storyboard-based application, you will often want to do a little preparation before navigation
- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender {
    // Get the new view controller using [segue destinationViewController].
    // Pass the selected object to the new view controller.
    
    if ([[segue identifier] isEqualToString:kSFNavegarAReporteEstadoActualEjecucionSegue])
    {
        // Get reference to the destination view controller
        SFReporteEstadoActualEjecucionRiegoViewController *vc = [segue destinationViewController];
        
        // Pass any objects to the view controller here, like...
        vc.ejecucion = self.ejecucion;
    }
    if ([[segue identifier] isEqualToString:kSFNavegarAReporteEstadoActualMedicionSegue])
    {
        // Get reference to the destination view controller
        SFReporteEstadoActualUltimaMedicionViewController *vc = [segue destinationViewController];
        
        // Pass any objects to the view controller here, like...
        vc.medicion = self.medicion;
    }
}

#pragma mark - Servicio

-(void) obtenerDatos {
    __weak typeof(self) weakSelf = self;
    
    SolicitudObtenerEstadoActualSector *solicitud = [SolicitudObtenerEstadoActualSector new];
    solicitud.idFinca = [[ContextoUsuario instance] fincaSeleccionada];
    solicitud.idSector = self.sector.idSector;
    
    [ServiciosModuloReportes obtenerEstadoActualSector:solicitud completionBlock:^(RespuestaServicioBase *respuesta) {
        [weakSelf hideActivityIndicator];
        
        if ([respuesta isKindOfClass:[RespuestaObtenerEstadoActualSector class]]) {
            RespuestaObtenerEstadoActualSector *respuestaObtenerEstadoActualSector = (RespuestaObtenerEstadoActualSector *)respuesta;
            
            if (respuestaObtenerEstadoActualSector.resultado) {
                
                self.numSectorLabel.text = [NSString stringWithFormat:@"%li",respuestaObtenerEstadoActualSector.nroSector];
                self.descripcionSectorLabel.text = respuestaObtenerEstadoActualSector.descripcionSector;
                self.superficieLabel.text = [NSString stringWithFormat:@"%0.f", respuestaObtenerEstadoActualSector.superficieSector];
                self.modeloComponenteLabel.text = respuestaObtenerEstadoActualSector.componenteSensorSector.modelo;
                self.estadoComponenteLabel.text = respuestaObtenerEstadoActualSector.componenteSensorSector.estadoComponenteSensor;
                self.tipoMecanismoLabel.text = respuestaObtenerEstadoActualSector.mecanismoRiegoFincaSector.nombreTipoMecanismo;
                
                self.ejecucion = respuestaObtenerEstadoActualSector.ejecucionRiego;
                self.medicion = respuestaObtenerEstadoActualSector.ultimaMedicion;
            } else {
                [weakSelf handleErrorWithPromptTitle:@"Error obteniendo reporte" message:kErrorDesconocido withCompletion:^{
                }];
            }
        }
    } failureBlock:^(ErrorServicioBase *error) {
        [weakSelf hideActivityIndicator];
        [weakSelf handleErrorWithPromptTitle:@"Error obteniendo reporte" message:error.detalleError withCompletion:^{
        }];
    }];
}

@end
