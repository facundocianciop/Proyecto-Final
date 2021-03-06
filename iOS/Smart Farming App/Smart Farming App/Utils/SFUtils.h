//
//  SFUtils.h
//  Smart Farming App
//
//  Created by Facundo Palma on 10/10/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "SFConstantesComunes.h"

@interface SFUtils : NSObject

#pragma mark - Color

+ (UIColor *)colorFromHexString:(NSString *)hexString alpha:(CGFloat)alpha;

+(UIColor *)primaryColor;
+(UIColor *)secondaryColor;
+(UIColor *)formCellColor;
+(UIColor *)formCellErrorColor;

#pragma mark - Font

#pragma mark - Sizing

#pragma mark - Dates

+(NSString *)formatDateDDMMYYYY:(NSDate *) aDate;
+(NSString *)formatDateYYYYMMDD:(NSDate *) aDate;
+(NSString *)formatDateDDMMYYYYTime:(NSDate *) aDate;

+(NSDate *)dateFromStringYYYYMMDD:(NSString *) dateString;
+(NSDate *)dateFromStringYYYYMMDDWithTime:(NSString *) dateString;

@end
