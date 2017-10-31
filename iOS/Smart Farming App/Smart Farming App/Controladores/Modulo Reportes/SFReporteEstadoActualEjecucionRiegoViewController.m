//
//  SFReporteEstadoActualEjecucionRiegoViewController.m
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/31/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFReporteEstadoActualEjecucionRiegoViewController.h"

@interface SFReporteEstadoActualEjecucionRiegoViewController ()

@property (strong, nonatomic) IBOutlet UILabel *estadoLabel;
@property (strong, nonatomic) IBOutlet UILabel *detalleLabel;
@property (strong, nonatomic) IBOutlet UILabel *aguaUtilizadaLabel;
@property (strong, nonatomic) IBOutlet UILabel *duracionMinLabel;
@property (strong, nonatomic) IBOutlet UILabel *duracionSegLabel;
@property (strong, nonatomic) IBOutlet UILabel *fechaHoraInicioLabel;
@property (strong, nonatomic) IBOutlet UILabel *fechaHoraFinProgramada;

@end

@implementation SFReporteEstadoActualEjecucionRiegoViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view.
}

-(void)viewWillAppear:(BOOL)animated {
    
    [self actualizarDatosPantalla:self.ejecucion];
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
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
        self.fechaHoraFinProgramada.text = [SFUtils formatDateDDMMYYYYTime:ejecucion.fechaHoraFinalProgramada];
    }
}

@end
