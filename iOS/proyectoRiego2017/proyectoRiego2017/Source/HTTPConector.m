//
//  HTTPConector.m
//  proyectoRIego2017
//
//  Created by Facundo José Palma on 9/21/17.
//  Copyright © 2017 Facundo José Palma. All rights reserved.
//

#import "HTTPConector.h"

#import <AFNetworking.h>
#import <AFHTTPSessionManager.h>

#define BASE_URL    @"https://comercial.bolsamza.com.ar/comercial_mobile/" //@"http://190.15.203.5/comercial_android/"
#define TEXT_HTML   @"text/html"
#define PHP_SUFIX   @".php"

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
    
    NSString *operationName = [operation stringByAppendingString:PHP_SUFIX];
    NSString *URL = [BASE_URL stringByAppendingString:operationName];
    
    if ([method isEqualToString:METHOD_GET]) {
        [self GET:URL withParameters:parameters completionBlock:completionBlock failureBlock:failureBlock];
    }
    else if ([method isEqualToString:METHOD_POST]) {
        [self POST:URL withParameters:parameters completionBlock:completionBlock failureBlock:failureBlock];
    }
}

#pragma mark - Internal

-(void)configureSessionManager {
    self.sessionManager = [AFHTTPSessionManager manager];
    self.sessionManager.responseSerializer.acceptableContentTypes = [self.sessionManager.responseSerializer.acceptableContentTypes setByAddingObject:TEXT_HTML];
}

-(void)GET:(NSString *)URL withParameters:(NSDictionary *)parameters completionBlock:(HTTPOperationCompletionBlock)completionBlock failureBlock:(HTTPOperationFailureBlock)failureBlock {
    
    [self.sessionManager POST:URL parameters:parameters progress:nil success:^(NSURLSessionDataTask * _Nonnull task, id  _Nullable responseObject){
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

#pragma mark - Ejemplo uso

-(void)test {
    NSString *url = [BASE_URL stringByAppendingString:[@"login" stringByAppendingString:PHP_SUFIX]];
    
    NSMutableDictionary *parameters = [NSMutableDictionary new];
    [parameters setObject:@"FAKE_PASSWORD" forKey:@"login_password"];
    [parameters setObject:@"FAKE_USERNAME" forKey:@"login_usuario"];
    
    AFHTTPSessionManager *manager = [AFHTTPSessionManager manager];
    
    [manager GET:url parameters:parameters progress:nil success:^(NSURLSessionTask *task, id responseObject) {
        NSLog(@"JSON: %@", responseObject);
    } failure:^(NSURLSessionTask *operation, NSError *error) {
        NSLog(@"Error: %@", error);
    }];
}

@end
