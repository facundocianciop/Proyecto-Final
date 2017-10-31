//
//  SFDetallesMecanismoRiegoViewController.m
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/20/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFDetallesMecanismoRiegoViewController.h"

#import "SFEjecucionRiego.h"
#import "ServiciosModuloRiego.h"

@interface SFDetallesMecanismoRiegoViewController ()

@property (weak, nonatomic) IBOutlet UILabel *estadoLabel;
@property (weak, nonatomic) IBOutlet UILabel *detalleLabel;
@property (weak, nonatomic) IBOutlet UILabel *aguaUtilizadaLabel;
@property (weak, nonatomic) IBOutlet UILabel *duracionMinLabel;
@property (weak, nonatomic) IBOutlet UILabel *duracionSegLabel;
@property (weak, nonatomic) IBOutlet UILabel *fechaHoraInicioLabel;
@property (weak, nonatomic) IBOutlet UILabel *fechaYHoraProgamadaFinLabel;


@end

@implementation SFDetallesMecanismoRiegoViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view.
}

-(void)viewWillAppear:(BOOL)animated {
    [self obtenerDatosEjecucion];
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

/*
#pragma mark - Navigation

// In a storyboard-based application, you will often want to do a little preparation before navigation
- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender {
    // Get the new view controller using [segue destinationViewController].
    // Pass the selected object to the new view controller.
}
*/
#pragma mark - servicio

-(void)obtenerDatosEjecucion {
    
    __weak typeof(self) weakSelf = self;
    
    SolicitudObtenerRiegoEnEjecucionMecanismoRiegoFincaSector *solicitud = [SolicitudObtenerRiegoEnEjecucionMecanismoRiegoFincaSector new];
    solicitud.idFinca = [[ContextoUsuario instance] fincaSeleccionada];
    solicitud.idMecanismoRiegoFincaSector = self.mecanismoRiego.idMecanismoRiegoFincaSector;
    
    [self showActivityIndicator];
    [ServiciosModuloRiego obtenerRiegoEnEjecucionMecanismoRiegoFincaSector:solicitud completionBlock:^(RespuestaServicioBase *respuesta) {
        [weakSelf hideActivityIndicator];
        
        if ([respuesta isKindOfClass:[RespuestaObtenerRiegoEnEjecucionMecanismoRiegoFincaSector class]]) {
            RespuestaObtenerRiegoEnEjecucionMecanismoRiegoFincaSector *respuestaObtenerRiegoEnEjecucionMecanismoRiegoFincaSector = (RespuestaObtenerRiegoEnEjecucionMecanismoRiegoFincaSector *)respuesta;
            
            if (respuestaObtenerRiegoEnEjecucionMecanismoRiegoFincaSector.resultado) {
                
                if (respuestaObtenerRiegoEnEjecucionMecanismoRiegoFincaSector.ejecucionRiego) {
                    [weakSelf actualizarDatosPantalla:respuestaObtenerRiegoEnEjecucionMecanismoRiegoFincaSector.ejecucionRiego];
                } else {
                    [self userInformationPrompt:@"Este mecanismo no esta regando"];
                    [self limpiarDatosPantalla];
                }
                
            } else {
                [weakSelf handleErrorWithPromptTitle:@"Error obteniendo ejecucion riego" message:kErrorDesconocido withCompletion:^{
                }];
            }
        }
    } failureBlock:^(ErrorServicioBase *error) {
        [weakSelf hideActivityIndicator];
        [weakSelf handleErrorWithPromptTitle:@"Error obteniendo ejecucion riego" message:error.detalleError withCompletion:^{
        }];
    }];
}

-(void)servicioInicarRiego {
    __weak typeof(self) weakSelf = self;
    
    SolicitudIniciarRiegoManualmente *solicitud = [SolicitudIniciarRiegoManualmente new];
    solicitud.idFinca = [[ContextoUsuario instance] fincaSeleccionada];
    solicitud.idMecanismoRiegoFincaSector = self.mecanismoRiego.idMecanismoRiegoFincaSector;
    
    [self showActivityIndicator];
    [ServiciosModuloRiego iniciarRiegoManualmente:solicitud completionBlock:^(RespuestaServicioBase *respuesta) {
        [weakSelf hideActivityIndicator];
        
        if ([respuesta isKindOfClass:[RespuestaIniciarRiegoManualmente class]]) {
            RespuestaIniciarRiegoManualmente *respuestaIniciarRiegoManualmente = (RespuestaIniciarRiegoManualmente *)respuesta;
            
            if (respuestaIniciarRiegoManualmente.resultado) {
                
                if (respuestaIniciarRiegoManualmente.ejecucionRiego) {
                    [weakSelf actualizarDatosPantalla:respuestaIniciarRiegoManualmente.ejecucionRiego];
                } else {
                    [self userInformationPrompt:@"Este mecanismo no esta regando"];
                    [self limpiarDatosPantalla];
                }
                
            } else {
                [weakSelf handleErrorWithPromptTitle:@"Error iniciando ejecucion de riego" message:kErrorDesconocido withCompletion:^{
                }];
            }
        }
    } failureBlock:^(ErrorServicioBase *error) {
        [weakSelf hideActivityIndicator];
        [weakSelf handleErrorWithPromptTitle:@"Error iniciando ejecucion de riego" message:error.detalleError withCompletion:^{
        }];
    }];
}

-(void)servicioPausarRiego {
    __weak typeof(self) weakSelf = self;
    
    SolicitudPausarRiegoManualmente *solicitud = [SolicitudPausarRiegoManualmente new];
    solicitud.idFinca = [[ContextoUsuario instance] fincaSeleccionada];
    solicitud.idMecanismoRiegoFincaSector = self.mecanismoRiego.idMecanismoRiegoFincaSector;
    
    [self showActivityIndicator];
    [ServiciosModuloRiego pausarRiegoManualmente:solicitud completionBlock:^(RespuestaServicioBase *respuesta) {
        [weakSelf hideActivityIndicator];
        
        if ([respuesta isKindOfClass:[RespuestaPausarRiegoManualmente class]]) {
            RespuestaPausarRiegoManualmente *respuestaPausarRiegoManualmente = (RespuestaPausarRiegoManualmente *)respuesta;
            
            if (respuestaPausarRiegoManualmente.resultado) {
                
                if (respuestaPausarRiegoManualmente.ejecucionRiego) {
                    [weakSelf actualizarDatosPantalla:respuestaPausarRiegoManualmente.ejecucionRiego];
                } else {
                    [self userInformationPrompt:@"Este mecanismo no esta regando"];
                    [self limpiarDatosPantalla];
                }
                
            } else {
                [weakSelf handleErrorWithPromptTitle:@"Error pausando ejecucion de riego" message:kErrorDesconocido withCompletion:^{
                }];
            }
        }
    } failureBlock:^(ErrorServicioBase *error) {
        [weakSelf hideActivityIndicator];
        [weakSelf handleErrorWithPromptTitle:@"Error pausando ejecucion de riego" message:error.detalleError withCompletion:^{
        }];
    }];
}

-(void)servicioCancelarRiego {
    __weak typeof(self) weakSelf = self;
    
    SolicitudCancelarRiegoManualmente *solicitud = [SolicitudCancelarRiegoManualmente new];
    solicitud.idFinca = [[ContextoUsuario instance] fincaSeleccionada];
    solicitud.idMecanismoRiegoFincaSector = self.mecanismoRiego.idMecanismoRiegoFincaSector;
    
    [self showActivityIndicator];
    [ServiciosModuloRiego cancelarRiegoManualmente:solicitud completionBlock:^(RespuestaServicioBase *respuesta) {
        [weakSelf hideActivityIndicator];
        
        if ([respuesta isKindOfClass:[RespuestaCancelarRiegoManualmente class]]) {
            RespuestaCancelarRiegoManualmente *respuestaCancelarRiegoManualmente = (RespuestaCancelarRiegoManualmente *)respuesta;
            
            if (respuestaCancelarRiegoManualmente.resultado) {
                
                if (respuestaCancelarRiegoManualmente.ejecucionRiego) {
                    [weakSelf actualizarDatosPantalla:respuestaCancelarRiegoManualmente.ejecucionRiego];
                } else {
                    [self userInformationPrompt:@"Este mecanismo no esta regando"];
                    [self limpiarDatosPantalla];
                }
                
            } else {
                [weakSelf handleErrorWithPromptTitle:@"Error cancelando ejecucion de riego" message:kErrorDesconocido withCompletion:^{
                }];
            }
        }
    } failureBlock:^(ErrorServicioBase *error) {
        [weakSelf hideActivityIndicator];
        [weakSelf handleErrorWithPromptTitle:@"Error cancelando ejecucion de riego" message:error.detalleError withCompletion:^{
        }];
    }];
}

#pragma mark - privado

-(void) actualizarDatosPantalla:(SFEjecucionRiego*)ejecucion {
    
    if ([ejecucion.nombreEstadoEjecucionRiego isEqualToString:kEstadoRiegoEjecucion]) {
        self.estadoLabel.text = @"En ejecucion";
    } else if ([ejecucion.nombreEstadoEjecucionRiego isEqualToString:kEstadoRiegoPausado]){
        self.estadoLabel.text = @"Pausado";
    } else if ([ejecucion.nombreEstadoEjecucionRiego isEqualToString:kEstadoRiegoCancelado]){
        self.estadoLabel.text = @"Cancelado";
    } else if ([ejecucion.nombreEstadoEjecucionRiego isEqualToString:kEstadoRiegoFinalizado]){
        self.estadoLabel.text = @"Finalizado";
    }
    
    self.detalleLabel.text = ejecucion.detalle;
    self.aguaUtilizadaLabel.text = [NSString stringWithFormat:@"%.2f", ejecucion.cantidadAguaUtilizadaLitros];
    self.duracionMinLabel.text = [NSString stringWithFormat:@"%.0f", ejecucion.duracionActualMinutos];
    self.duracionSegLabel.text = [NSString stringWithFormat:@"%.0f", ejecucion.duracionActualSegundos];
    if (ejecucion.fechaHoraInicio) {
        self.fechaHoraInicioLabel.text = [SFUtils formatDateDDMMYYYYTime:ejecucion.fechaHoraInicio];
    }
    if (ejecucion.fechaHoraFinalProgramada) {
        self.fechaYHoraProgamadaFinLabel.text = [SFUtils formatDateDDMMYYYYTime:ejecucion.fechaHoraFinalProgramada];
    }
}

-(void) limpiarDatosPantalla {
    
    self.estadoLabel.text = @"Finalizado";
    self.detalleLabel.text = @"-";
    self.aguaUtilizadaLabel.text = @"-";
    self.duracionMinLabel.text = @"-";
    self.duracionSegLabel.text = @"-";
    self.fechaHoraInicioLabel.text = @"-";
    self.fechaYHoraProgamadaFinLabel.text = @"-";

}

#pragma mark - acciones

- (IBAction)actualizar:(id)sender {
    [self obtenerDatosEjecucion];
}

- (IBAction)iniciarRiego:(id)sender {
    [self servicioInicarRiego];
}

- (IBAction)pausarRiego:(id)sender {
    [self servicioPausarRiego];
}

- (IBAction)cancelarRiego:(id)sender {
    [self servicioCancelarRiego];
}

@end
