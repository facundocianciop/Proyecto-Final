//
//  RespuestaObtenerInformeHistoricoHeladas.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 10/24/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "RespuestaServicioBase.h"

#import "SFOcurrenciaEventoPersonalizado.h"

@interface RespuestaObtenerInformeHistoricoHeladas : RespuestaServicioBase

@property (strong, nonatomic) NSArray<SFOcurrenciaEventoPersonalizado*> *listaOcurrenciasHelada;

@end
