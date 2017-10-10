//
//  ContextoUsuario.m
//  proyectoRIego2017
//
//  Created by Facundo José Palma on 9/21/17.
//  Copyright © 2017 Facundo José Palma. All rights reserved.
//

#import "ContextoUsuario.h"

@interface ContextoUsuario ()

@property (nonatomic, strong) NSString  *sessionId;
@property (nonatomic, strong) NSString  *clientDescription;       //RAZON SOCIAL
@property (nonatomic, assign) long      userId;
@property (nonatomic, assign) long      clientId;

@end

@implementation ContextoUsuario

static ContextoUsuario *userContext = nil;

+(instancetype)instanceWithSessionId:(NSString *)sessionId
                              userId:(long)userId
                            clientId:(long)clientId
                   clientDescription:(NSString *)clientDescription {
    
    // No se puede usar el dispatch_once snippet
    // Si un usuario se cierra sesion y otro se logea, puede ser que
    // datos incorrectos
    
    if (!userContext){
        userContext = [ContextoUsuario new];
        userContext.sessionId = sessionId;
        userContext.userId = userId;
        userContext.clientId = clientId;
        userContext.clientDescription = clientDescription;
    }
    return userContext;
}

+(instancetype)instance {
    
    ContextoUsuario *userContext = [self instanceWithSessionId:nil userId:NSNotFound clientId:NSNotFound clientDescription:@""];
    
    if (!userContext.sessionId || userContext.userId == NSNotFound || userContext.clientId == NSNotFound){
        //[NSException raise:@"BCUserContext: User context hasn't been initialized properly. Param: sessionId OR Param:userId may be uninitialized." format:@""];
        NSLog(@"ContextoUsuario: El contexto de usario no se inicio correctamente. Param: sessionId O Param:userId puede que no esten inicializados.");
    }
    return  userContext;
}

#pragma mark - Public

-(NSString *)currentSessionId {
    return self.sessionId;
}

-(long)currentUserId {
    return self.userId;
}

-(long)currentClientId {
    return self.clientId;
}

-(NSString *)currentClientDescription {
    return self.clientDescription;
}

-(void)invalidateContext {
    self.sessionId = nil;
    self.userId = NSNotFound;
    self.clientId = NSNotFound;
    self.clientDescription = nil;
    userContext = nil;
}

@end
