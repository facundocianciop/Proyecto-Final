//
//  SFTableViewControllerBase.h
//  Smart Farming App
//
//  Created by Facundo Palma on 10/14/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import <UIKit/UIKit.h>

#import "SFViewControllerBase.h"

static NSString *kTableViewCellIdentifier = @"Cell";

@interface SFTableViewControllerBase : SFViewControllerBase <UITableViewDataSource, UITableViewDelegate>

@property (strong, nonatomic) UITableView *tableView;
@property (strong, nonatomic) NSArray *tableViewItemsArray;
@property (strong, nonatomic) UILabel *emptyTableViewMessageLabel;
@property (strong, nonatomic) UIRefreshControl *refreshControl;

-(void)configurarTabla;
-(void)refreshAction;
-(void)beginTableViewDataLoading;
-(void)loadingTableViewDataDidEnd;
-(void)loadingTableViewDataFailed;

@end
