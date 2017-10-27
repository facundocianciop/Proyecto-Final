//
//  SFDatosFincaHelper.m
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/27/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFDatosFincaHelper.h"

#import "ServiciosModuloFinca.h"

@implementation SFDatosFincaHelper

+(void)obtenerPermisosFinca:(long)idFinca withCompletion:(void(^)(BOOL))completionBlock {
    
    SolicitudBuscarFincaId *solicitud = [SolicitudBuscarFincaId new];
    solicitud.idFinca = idFinca;
    
    __weak typeof(self) weakSelf = self;
    [self showActivityIndicator];
    [ServiciosModuloFinca buscarFincaId:solicitud completionBlock:^(RespuestaServicioBase *respuesta) {
        [weakSelf hideActivityIndicator];
        
        if ([respuesta isKindOfClass:[RespuestaBuscarFincaId class]]) {
            RespuestaBuscarFincaId *respuestaMostrarFincas = (RespuestaBuscarFincaId *)respuesta;
            
            if (respuestaMostrarFincas.resultado) {
                
                
                
                
                
                [[ContextoUsuario instance] seleccionarFinca:finca.idFinca];
                [self performSegueWithIdentifier:kSFNavegarASeccionFincaSegue sender:self];
                
                
                weakSelf.tableViewItemsArray = respuestaMostrarFincas.fincas;
                [weakSelf loadingTableViewDataDidEnd];
            } else {
                [weakSelf loadingTableViewDataFailed];
                [weakSelf handleErrorWithPromptTitle:kErrorObteniendoDatosFinca message:kErrorDesconocido withCompletion:^{
                }];
            }
        }
    } failureBlock:^(ErrorServicioBase *error) {
        [weakSelf hideActivityIndicator];
        [weakSelf handleErrorWithPromptTitle:kErrorObteniendoDatosFinca message:error.detalleError withCompletion:^{
            [weakSelf loadingTableViewDataFailed];
        }];
    }];
    
}


@end
