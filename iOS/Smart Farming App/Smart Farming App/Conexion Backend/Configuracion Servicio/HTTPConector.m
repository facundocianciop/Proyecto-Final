//
//  HTTPConector.m
//  Smart Farming App
//
//  Created by Facundo José Palma on 9/21/17.
//  Copyright © 2017 Facundo José Palma. All rights reserved.
//

#import "HTTPConector.h"

#import <AFNetworking.h>
#import <AFHTTPSessionManager.h>

#define BASE_URL    @"http://127.0.0.1:8000/riegoInteligente/"
#define TEXT_HTML   @"text/html"
#define APPLICATION_JSON   @"application/json"

@interface HTTPConector ()

- (instancetype)init;

@property (nonatomic, strong) AFHTTPSessionManager *sessionManager;

@end

@implementation HTTPConector

#pragma mark - Initialization

+(instancetype)instance {
    static HTTPConector *httpConector;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        httpConector = [[HTTPConector alloc] init];
    });
    return httpConector;
}

- (instancetype)init {
    self = [super init];
    if (self) {
        [self configureSessionManager];
    }
    return self;
}

#pragma mark - Public

-(void)httpOperation:(NSString *)operation
              method:(NSString *)method
      withParameters:(NSDictionary *)parameters
     completionBlock:(HTTPOperationCompletionBlock)completionBlock
        failureBlock:(HTTPOperationFailureBlock)failureBlock {
    
    NSString *operationName = [operation stringByAppendingString:@"/"];
    NSString *URL = [BASE_URL stringByAppendingString:operationName];
    
    if ([method isEqualToString:METHOD_GET]) {
        [self GET:URL withParameters:parameters completionBlock:completionBlock failureBlock:failureBlock];
    }
    else if ([method isEqualToString:METHOD_DELETE]) {
        [self DELETE:URL withParameters:parameters completionBlock:completionBlock failureBlock:failureBlock];
    }
    else if ([method isEqualToString:METHOD_POST]) {
        [self POST:URL withParameters:parameters completionBlock:completionBlock failureBlock:failureBlock];
    }
}

#pragma mark - Internal

-(void)configureSessionManager {
    self.sessionManager = [AFHTTPSessionManager manager];
    self.sessionManager.responseSerializer.acceptableContentTypes = [self.sessionManager.responseSerializer.acceptableContentTypes setByAddingObject:APPLICATION_JSON];
}

-(void)GET:(NSString *)URL withParameters:(NSDictionary *)parameters completionBlock:(HTTPOperationCompletionBlock)completionBlock failureBlock:(HTTPOperationFailureBlock)failureBlock {
    
    [self.sessionManager POST:URL parameters:parameters progress:nil success:^(NSURLSessionDataTask * _Nonnull task, id  _Nullable responseObject){
        completionBlock(responseObject);
    } failure:^(NSURLSessionDataTask * _Nullable task, NSError * _Nonnull error) {
        [self handleServiceError:task error:error completionBlock:completionBlock failureBlock:failureBlock];
    }];
}

-(void)DELETE:(NSString *)URL withParameters:(NSDictionary *)parameters completionBlock:(HTTPOperationCompletionBlock)completionBlock failureBlock:(HTTPOperationFailureBlock)failureBlock {
    
    [self.sessionManager DELETE:URL parameters:parameters success:^(NSURLSessionDataTask * _Nonnull task, id  _Nullable responseObject) {
        completionBlock(responseObject);
    } failure:^(NSURLSessionDataTask * _Nullable task, NSError * _Nonnull error) {
        [self handleServiceError:task error:error completionBlock:completionBlock failureBlock:failureBlock];
    }];
}

-(void)POST:(NSString *)URL withParameters:(NSDictionary *)parameters completionBlock:(HTTPOperationCompletionBlock)completionBlock failureBlock:(HTTPOperationFailureBlock)failureBlock {
    
    [self.sessionManager POST:URL parameters:parameters progress:nil success:^(NSURLSessionDataTask * _Nonnull task, id  _Nullable responseObject) {
        completionBlock(responseObject);
    } failure:^(NSURLSessionDataTask * _Nullable task, NSError * _Nonnull error) {
        [self handleServiceError:task error:error completionBlock:completionBlock failureBlock:failureBlock];
    }];
}

-(void)handleServiceError:(NSURLSessionDataTask *) task error:(NSError *)error completionBlock:(HTTPOperationCompletionBlock)completionBlock failureBlock:(HTTPOperationFailureBlock)failureBlock {
    
    // Algunas llamadas pueden fallar y entrar por el success block. Controlar codigo de respuesta.
    // Example: cerrar_sesion
    
    if (!task){
        failureBlock(error);
        return;
    }
    
    NSHTTPURLResponse* response = (NSHTTPURLResponse*)task.response;
    if (response.statusCode == 200){
        completionBlock(nil);
    }else{
        failureBlock(error);
    }
}

@end
