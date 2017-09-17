import { Component } from '@angular/core';
import { CompleterService, CompleterData } from 'ng2-completer';
 
@Component({
  selector: 'my-component',
  template: `<h1>Search color</h1>
            <ng2-completer [(ngModel)]="searchStr" [datasource]="dataService" [minSearchLength]="0"></ng2-completer>
            <h1>Search captain</h1>
            <ng2-completer [(ngModel)]="captain" [datasource]="captains" [minSearchLength]="0"></ng2-completer>`
})
export class MyComponent {
 
  protected searchStr: string;
  protected captain: string;
  protected dataService: CompleterData;
  protected searchData = [
    { color: 'red', value: '#f00' },
    { color: 'green', value: '#0f0' },
    { color: 'blue', value: '#00f' },
    { color: 'cyan', value: '#0ff' },
    { color: 'magenta', value: '#f0f' },
    { color: 'yellow', value: '#ff0' },
    { color: 'black', value: '#000' }
  ];
  protected captains = ['James T. Kirk', 'Benjamin Sisko', 'Jean-Luc Picard', 'Spock', 'Jonathan Archer', 'Hikaru Sulu', 'Christopher Pike', 'Rachel Garrett' ];
 
  constructor(private completerService: CompleterService) {
    this.dataService = completerService.local(this.searchData, 'color', 'color');
  }
}