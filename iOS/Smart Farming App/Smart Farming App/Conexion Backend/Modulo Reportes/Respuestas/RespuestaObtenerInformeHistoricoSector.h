//
//  RespuestaObtenerInformeHistoricoSector.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/24/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "RespuestaServicioBase.h"

#import "DTOMedicionClimatica.h"
#import "DTOComponenteMedicion.h"

@interface RespuestaObtenerInformeHistoricoSector : RespuestaServicioBase

@property (strong, nonatomic) NSArray<DTOComponenteMedicion*> *listaComponenteMediciones; //componenteMedicionListaMediciones
@property (strong, nonatomic) NSArray<DTOMedicionClimatica*> *listaMedicionesClimaticas;

@end
