//
//  PRUtils.h
//  proyectoRiego2017
//
//  Created by Facundo José Palma on 9/21/17.
//  Copyright © 2017 Facundo José Palma. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface PRUtils : NSObject

#pragma mark - Color

+(UIColor *)primaryColor;

+(UIColor *)secondaryColor;

#pragma mark - Font

#pragma mark - Sizing

#pragma mark - Dates

+(NSString *)formatDateDDMMYYYY:(NSDate *) aDate;

@end
