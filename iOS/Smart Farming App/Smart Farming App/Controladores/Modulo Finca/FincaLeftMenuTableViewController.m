//
//  FincaLeftMenuTableViewController.m
//  Smart Farming App
//
//  Created by Facundo Palma on 10/15/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "FincaLeftMenuTableViewController.h"

@interface FincaLeftMenuTableViewController ()

@end

@implementation FincaLeftMenuTableViewController

static NSString *kMenuItemInfoFinca = @"CellInfoFinca";
static NSString *kMenuItemSectores = @"CellSectores";
static NSString *kMenuItemRiego = @"CellRiego";
static NSString *kMenuItemReportes = @"CellReportes";
static NSString *kMenuItemVolver = @"CellVolver";

- (void)viewDidLoad {
    [super viewDidLoad];
    
    // Uncomment the following line to preserve selection between presentations.
    // self.clearsSelectionOnViewWillAppear = NO;
    
    // Uncomment the following line to display an Edit button in the navigation bar for this view controller.
    // self.navigationItem.rightBarButtonItem = self.editButtonItem;
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

/*
 #pragma mark - Navigation
 
 // In a storyboard-based application, you will often want to do a little preparation before navigation
 - (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender {
 // Get the new view controller using [segue destinationViewController].
 // Pass the selected object to the new view controller.
 }
 */

#pragma mark - Table view data source

-(void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath {
    
    UITableViewCell *cell = [self tableView:tableView cellForRowAtIndexPath:indexPath];
    
    if ([cell.reuseIdentifier isEqualToString:kMenuItemInfoFinca]) {
        
    }
    else if ([cell.reuseIdentifier isEqualToString:kMenuItemSectores]) {
        
    }
    else if ([cell.reuseIdentifier isEqualToString:kMenuItemRiego]) {
        
    }
    else if ([cell.reuseIdentifier isEqualToString:kMenuItemReportes]) {
        
    }
    else if ([cell.reuseIdentifier isEqualToString:kMenuItemVolver]) {
        [self.navigationController popViewControllerAnimated:YES];
    }
}

@end
