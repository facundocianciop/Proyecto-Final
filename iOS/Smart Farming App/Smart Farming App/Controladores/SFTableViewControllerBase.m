//
//  SFTableViewControllerBase.m
//  Smart Farming App
//
//  Created by Facundo Palma on 10/14/17.
//  Copyright © 2017 Smart Farming. All rights reserved.
//

#import "SFTableViewControllerBase.h"

@interface SFTableViewControllerBase ()

@end

@implementation SFTableViewControllerBase

- (void)viewDidLoad {
    [super viewDidLoad];
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

#pragma mark - Acciones

-(void)refreshAction {
    NSLog(@"No hay accion definida");
}

-(void)loadingDataEnded {
    [self.tableView reloadData];
    if (self.refreshControl) {
        [self.refreshControl endRefreshing];
    }
}

#pragma mark - Configurar tabla

-(void)configurarTabla {
    
    self.refreshControl = [[UIRefreshControl alloc] init];
    self.refreshControl.backgroundColor = [SFUtils primaryColor];
    self.refreshControl.tintColor = [UIColor whiteColor];
    [self.refreshControl addTarget:self
                            action:@selector(refreshAction)
                  forControlEvents:UIControlEventValueChanged];
    self.tableView.refreshControl = self.refreshControl;
    
    self.tableView.backgroundView = self.emptyTableViewMessageLabel;
    [self.tableView registerClass:[UITableViewCell class] forCellReuseIdentifier:kTableViewCellIdentifier];
}

#pragma mark - Table view data source/delegate

- (NSInteger)numberOfSectionsInTableView:(UITableView *)tableView {
    
    if ([self.tableViewItemsArray count]>0) {
        self.emptyTableViewMessageLabel.hidden = YES;
        self.tableView.separatorStyle = UITableViewCellSeparatorStyleSingleLineEtched;
        return 1;
    } else {
        self.emptyTableViewMessageLabel.hidden = NO;
        self.tableView.separatorStyle = UITableViewCellSeparatorStyleNone;
    }
    return 0;
}

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section {
    return [self.tableViewItemsArray count];
}

- (nonnull UITableViewCell *)tableView:(nonnull UITableView *)tableView cellForRowAtIndexPath:(nonnull NSIndexPath *)indexPath {
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:kTableViewCellIdentifier forIndexPath:indexPath];
    
    cell.textLabel.text = @"Empty cell";
    
    return cell;
}

@end
