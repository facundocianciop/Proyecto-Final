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
        this.cerrarSesionService.cerrarSesion()
        .then(
            response => this.sesion=response
        )
        .then(
            response=> this.router.navigate(['/login'])
        );
            
            
            
        
    }


}
