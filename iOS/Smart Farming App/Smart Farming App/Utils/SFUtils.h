//
//  SFUtils.h
//  Smart Farming App
//
//  Created by Facundo Palma on 10/10/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface SFUtils : NSObject

#pragma mark - Color

+(UIColor *)primaryColor;

+(UIColor *)secondaryColor;

#pragma mark - Font

#pragma mark - Sizing

#pragma mark - Dates

+(NSString *)formatDateDDMMYYYY:(NSDate *) aDate;

@end
