import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CerrarSesionService } from './cerrar.sesion.service';

@Component({
    selector:'app-cerrar-sesion',
    templateUrl: './cerrar.sesion.component.html',
    styleUrls:['./cerrar.sesion.component.css']
})

export class CerrarSesionComponent implements OnInit{
    sesion:Boolean;
    constructor(private router:Router,
                private cerrarSesionService:CerrarSesionService){

    }

    ngOnInit(){
        this.cerrarSesionService.cerrarSesion("cookie")
        .then(response => this.sesion=response);
        if(this.sesion==true){
            console.log("el usuario ha finalizado su sesion")
            this.router.navigate(['/login']);
            
        }
        else{
            console.log("error al cerrar sesion");
        }
    }


}
