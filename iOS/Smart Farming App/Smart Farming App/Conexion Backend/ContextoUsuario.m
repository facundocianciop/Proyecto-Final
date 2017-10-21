//
//  ContextoUsuario.m
//  Smart Farming App
//
//  Created by Facundo José Palma on 9/21/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "ContextoUsuario.h"

#import "HTTPConector.h"

@interface ContextoUsuario ()

@property (strong, nonatomic) NSString  *username;
@property (assign, nonatomic) long      fincaId;

@end

@implementation ContextoUsuario

static ContextoUsuario *userContext = nil;

+(instancetype)instanceWithUsername:(NSString *)username {
    // No se puede usar el dispatch_once snippet
    // Si un usuario se cierra sesion y otro se logea, puede ser que
    // datos incorrectos
    
    if (!userContext){
        userContext = [ContextoUsuario new];
        userContext.username = username;
    }
    return userContext;
}

+(instancetype)instance {
    
    ContextoUsuario *userContext = [ContextoUsuario instanceWithUsername:nil];
    
    if (!userContext.username){
        //[NSException raise:@"BCUserContext: User context hasn't been initialized properly. Param:idUsuario may be uninitialized." format:@""];
        NSLog(@"ContextoUsuario: El contexto de usario no se inicio correctamente. Param:username puede que no este inicializado.");
    }
    return  userContext;
}

#pragma mark - Public

-(NSString *)usuarioActual {
    return self.username;
}

-(void)seleccionarFinca:(long)fincaId {
    self.fincaId = fincaId;
}

-(long)fincaSeleccionada{
    return self.fincaId;
}

-(void)invalidateContext {
    
    [[HTTPConector instance] endSession];
    
    self.username = nil;
    self.fincaId = NSNotFound;
    userContext = nil;
}

@end
