//
//  SFSectorFinca.h
//  Smart Farming App
//
//  Created by Facundo Palma on 10/14/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface SFSectorFinca : NSObject

@property (assign, nonatomic) long idSector;
@property (assign, nonatomic) NSInteger numeroSector;

@property (strong, nonatomic) NSString *nombreSector;
@property (strong, nonatomic) NSString *descripcionSector;

@property (assign, nonatomic) NSInteger superficieSector;

@end
