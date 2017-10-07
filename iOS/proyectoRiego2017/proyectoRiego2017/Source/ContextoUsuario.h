//
//  ContextoUsuario.h
//  proyectoRIego2017
//
//  Created by Facundo José Palma on 9/21/17.
//  Copyright © 2017 Facundo José Palma. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface ContextoUsuario : NSObject

#pragma mark - Initialization

+(instancetype)instanceWithSessionId:(NSString *)sessionId
                              userId:(long)userId
                            clientId:(long)clientId
                   clientDescription:(NSString *)clientDescription;

+(instancetype)instance;

#pragma mark - Public

-(NSString *)currentSessionId;
-(long)currentUserId;
-(long)currentClientId;
-(NSString *)currentClientDescription;
-(void)invalidateContext;

@end
