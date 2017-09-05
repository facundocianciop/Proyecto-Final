import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
    selector:'app-recuperar',
    templateUrl: './recuperar.cuenta.component.html',
    styleUrls:['./recuperar.cuenta.component.css']
    
})

export class RecuperarCuentaComponent implements OnInit{
    divPrimero:Boolean;
    divSegundo:Boolean;
    divTercero:Boolean;
    constructor(private router:Router){

    }

    ngOnInit(){
        this.divPrimero=true;
        this.divSegundo=false;
        this.divTercero=false;

    }
    
    aprertarRegistrar(){
        console.log("estamos aca");
        this.router.navigate(['/login']);
    }

    aprertarCancelar(){
        console.log("estamos aca");
        this.router.navigate(['/login']);
    }
    obtenerDatosDivPrimero(){
        this.divPrimero=false;
        this.divSegundo=true;
    }
    obtenerDatosDivSegundo(){
        this.divSegundo=false;
        this.divTercero=true;
    }
    obtenerDatosDivTercero(){
        this.router.navigate(['/login']);
    }
}