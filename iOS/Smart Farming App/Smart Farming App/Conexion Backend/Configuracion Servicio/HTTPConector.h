//
//  HTTPConector.h
//  Smart Farming App
//
//  Created by Facundo José Palma on 9/21/17.
//  Copyright © 2017 Facundo José Palma. All rights reserved.
//

#import <Foundation/Foundation.h>

#define METHOD_GET  @"GET"
#define METHOD_POST @"POST"
#define METHOD_DELETE @"DELETE"

typedef void (^HTTPOperationCompletionBlock)(NSDictionary *responseObject);
typedef void (^HTTPOperationFailureBlock)(NSError *error);

@interface HTTPConector : NSObject

#pragma mark - Inicializacion

+(instancetype)instance;

#pragma mark - Publico

-(void)httpOperation:(NSString *)operation
              method:(NSString *)method
      withParameters:(NSDictionary *)parameters
     completionBlock:(HTTPOperationCompletionBlock)completionBlock
        failureBlock:(HTTPOperationFailureBlock)failureBlock;

@end
