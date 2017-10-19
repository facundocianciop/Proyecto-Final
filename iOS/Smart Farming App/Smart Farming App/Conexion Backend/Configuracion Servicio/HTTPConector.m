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

#import "ErrorServicioBase.h"

#define BASE_URL    @"http://127.0.0.1:8000/riegoInteligente/"

#define TEXT_HTML   @"text/html"

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

-(void)endSession {
    NSURL *url = [NSURL URLWithString:BASE_URL];
    NSArray *cookies = [[NSHTTPCookieStorage sharedHTTPCookieStorage] cookiesForURL:url];
    for (NSHTTPCookie *cookie in cookies)
    {
        [[NSHTTPCookieStorage sharedHTTPCookieStorage] deleteCookie:cookie];
    }
}

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
    else if ([method isEqualToString:METHOD_PUT]) {
        [self PUT:URL withParameters:parameters completionBlock:completionBlock failureBlock:failureBlock];
    } else {
        failureBlock([NSError new]);
    }
}

#pragma mark - Internal

-(void)configureSessionManager {
    self.sessionManager = [AFHTTPSessionManager manager];
    self.sessionManager.requestSerializer = [AFJSONRequestSerializer serializer];
    self.sessionManager.responseSerializer = [AFJSONResponseSerializer serializer];
    self.sessionManager.responseSerializer.acceptableContentTypes = [self.sessionManager.responseSerializer.acceptableContentTypes setByAddingObject:TEXT_HTML];
}

-(void)GET:(NSString *)URL withParameters:(NSDictionary *)parameters completionBlock:(HTTPOperationCompletionBlock)completionBlock failureBlock:(HTTPOperationFailureBlock)failureBlock {
    
    [self.sessionManager GET:URL parameters:parameters progress:nil success:^(NSURLSessionDataTask * _Nonnull task, id  _Nullable responseObject) {
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

-(void)PUT:(NSString *)URL withParameters:(NSDictionary *)parameters completionBlock:(HTTPOperationCompletionBlock)completionBlock failureBlock:(HTTPOperationFailureBlock)failureBlock {
    
    [self.sessionManager PUT:URL parameters:parameters success:^(NSURLSessionDataTask * _Nonnull task, id  _Nullable responseObject) {
        completionBlock(responseObject);
    } failure:^(NSURLSessionDataTask * _Nullable task, NSError * _Nonnull error) {
        [self handleServiceError:task error:error completionBlock:completionBlock failureBlock:failureBlock];
    }];
}

-(void)handleServiceError:(NSURLSessionDataTask *) task error:(NSError *)error completionBlock:(HTTPOperationCompletionBlock)completionBlock failureBlock:(HTTPOperationFailureBlock)failureBlock {
    
    NSHTTPURLResponse* response = (NSHTTPURLResponse*)task.response;
    ErrorServicioBase *errorServicio = nil;
    
    NSData *errorData = error.userInfo[AFNetworkingOperationFailingURLResponseDataErrorKey];
    if (errorData) {
        @try {
            NSDictionary *serializedData = [NSJSONSerialization JSONObjectWithData: errorData options:kNilOptions error:nil];
            
            errorServicio = [[ErrorServicioBase alloc] initWithDomain:error.domain code:response.statusCode userInfo:serializedData];
            errorServicio.codigoError = serializedData[KEY_ERROR_CODE];
            errorServicio.detalleError = serializedData[KEY_ERROR_DESCRIPTION];
        } @catch (NSException *exception) {
            errorServicio = [[ErrorServicioBase alloc] initWithDomain:error.domain code:error.code userInfo:error.userInfo];
            errorServicio.codigoError = [NSString stringWithFormat:@"%li", error.code];
            
            if ([error.domain isEqualToString:NSURLErrorDomain]) {
                errorServicio.detalleError = @"Error de comunicación con el servidor";
            } else {
                errorServicio.detalleError = error.userInfo[NSLocalizedDescriptionKey];
            }
        }
    } else {
        errorServicio = [[ErrorServicioBase alloc] initWithDomain:error.domain code:error.code userInfo:error.userInfo];
        errorServicio.codigoError = [NSString stringWithFormat:@"%li", error.code];
        
        if ([error.domain isEqualToString:NSURLErrorDomain]) {
            errorServicio.detalleError = @"Error de comunicación con el servidor";
        } else {
            errorServicio.detalleError = error.userInfo[NSLocalizedDescriptionKey];
        }
    }
    
    // Algunas llamadas pueden fallar y entrar por el success block. Controlar codigo de respuesta.
    // Ejemplo: cerrar_sesion
    if (!task){
        failureBlock(errorServicio);
        return;
    }
    if (response.statusCode == 200){
        completionBlock(nil);
    }else{
        failureBlock(errorServicio);
    }
}

@end
