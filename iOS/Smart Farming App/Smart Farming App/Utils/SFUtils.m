//
//  SFUtils.m
//  Smart Farming App
//
//  Created by Facundo Palma on 10/10/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFUtils.h"

@implementation SFUtils

#pragma mark - Color

+ (UIColor *)colorFromHexString:(NSString *)hexString alpha:(CGFloat)alpha {
    unsigned rgbValue = 0;
    NSScanner *scanner = [NSScanner scannerWithString:hexString];
    [scanner setScanLocation:1]; // bypass '#' character
    [scanner scanHexInt:&rgbValue];
    return [UIColor colorWithRed:((rgbValue & 0xFF0000) >> 16)/255.0 green:((rgbValue & 0xFF00) >> 8)/255.0 blue:(rgbValue & 0xFF)/255.0 alpha:alpha];
}

+(UIColor*)primaryColor {
    return [SFUtils colorFromHexString:kColorVerdeClaroHex alpha:1.0];
}

+(UIColor *)secondaryColor {
    return [SFUtils colorFromHexString:kColorCelesteHex alpha:1.0];
}

+(UIColor *)formCellColor {
    return [UIColor whiteColor];
}

+(UIColor *)formCellErrorColor {
    return [UIColor orangeColor];
}

#pragma mark - Font

#pragma mark - Sizing

#pragma mark - Dates

+(NSString *)formatDateDDMMYYYY:(NSDate *) aDate {
    NSDateFormatter *dateFormat = [[NSDateFormatter alloc] init];
    [dateFormat setDateFormat:@"dd/MM/YYYY"];
    return [dateFormat stringFromDate:aDate];
}

+(NSString *)formatDateYYYYMMDD:(NSDate *) aDate {
    NSDateFormatter *dateFormat = [[NSDateFormatter alloc] init];
    [dateFormat setDateFormat:@"YYYY-MM-dd"];
    return [dateFormat stringFromDate:aDate];
}

+(NSString *)formatDateDDMMYYYYTime:(NSDate *) aDate {
    NSDateFormatter *dateFormat = [[NSDateFormatter alloc] init];
    [dateFormat setDateFormat:@"dd/MM/YYYY - HH:mm:ss"];
    return [dateFormat stringFromDate:aDate];
}

+(NSDate *)dateFromStringYYYYMMDD:(NSString *) dateString {
    // Convert string to date object
    NSDateFormatter *dateFormat = [[NSDateFormatter alloc] init];
    [dateFormat setDateFormat:@"yyyy-MM-dd"];
    return [dateFormat dateFromString:dateString];
}

+(NSDate *)dateFromStringYYYYMMDDWithTime:(NSString *) dateString {
    // Convert string to date object
    NSDateFormatter *dateFormat = [[NSDateFormatter alloc] init];
    [dateFormat setDateFormat:@"yyyy-MM-dd'T'HH:mm:ss.SSSZ"];
    [dateFormat setTimeZone:[NSTimeZone timeZoneWithAbbreviation:@"America/Argentina/Buenos_Aires"]];
    NSDate *newDate = [dateFormat dateFromString:dateString];
    if (!newDate) {
        [dateFormat setDateFormat:@"yyyy-MM-dd'T'HH:mm:ssZ"];
        newDate = [dateFormat dateFromString:dateString];
    }
    return newDate;
}


@end
