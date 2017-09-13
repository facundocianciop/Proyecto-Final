import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import {NgbModule} from '@ng-bootstrap/ng-bootstrap';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
  
})
export class AppComponent implements OnInit {
  bodyInicio:Boolean;
  constructor(private router:Router){
    
  }
  ngOnInit(){
    this.bodyInicio=false;
  }
  apretarIngresar(){
    this.bodyInicio=false;
  }
}
