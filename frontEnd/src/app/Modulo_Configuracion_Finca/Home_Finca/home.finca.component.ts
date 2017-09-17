import { Component, OnInit, Input } from '@angular/core';
import { Router } from '@angular/router';
import { HomeFincaService, Finca, FincaUsuario } from './home.finca.service';

@Component({
    selector:'homeFinca',
    templateUrl: './home.finca.component.html',
    styleUrls:['./home.finca.component.css']
    
})

export class HomeFincaComponent implements OnInit{
    fincasPendientes:Finca[];
    fincasUsuario:FincaUsuario[];
    fincasEncargado:Finca[];
    
    constructor(private router:Router,
                private homeFincaService:HomeFincaService){

    }

    ngOnInit(){
        this.homeFincaService.obtenerFincasPendientes()
                             .then(response=>this.fincasPendientes=response);
        /*this.homeFincaService.obtenerFincasUsuario()
                             .then(response=>this.fincasUsuario=response);
        this.homeFincaService.obtenerFincasEncargado()
                             .then(response=>this.fincasEncargado=response);*/
    }
}
