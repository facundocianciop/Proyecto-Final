//
//  PRUtils.m
//  proyectoRiego2017
//
//  Created by Facundo José Palma on 9/21/17.
//  Copyright © 2017 Facundo José Palma. All rights reserved.
//

#import "PRUtils.h"

@implementation PRUtils

+(UIColor*)primaryColor {
    return [UIColor colorWithRed:163/255.0 green:145/255.0 blue:98/255.0 alpha:0.8];
}

+(UIColor *)secondaryColor {
    return [UIColor colorWithRed:1 green:1 blue:1 alpha:0.8];
}

#pragma mark - Font

#pragma mark - Sizing

#pragma mark - Dates

+(NSString *)formatDateDDMMYYYY:(NSDate *) aDate {
    NSDateFormatter *dateFormat = [[NSDateFormatter alloc] init];
    [dateFormat setDateFormat:@"dd/MM/YYYY"];
    return [dateFormat stringFromDate:aDate];
}

@end
