import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
    selector:'app-home',
    templateUrl: './home.finca.component.html',
    styleUrls:['./home.finca.component.css']
    
})

export class HomeFincaComponent implements OnInit{
    constructor(private router:Router){

    }

    ngOnInit(){

    }
}
