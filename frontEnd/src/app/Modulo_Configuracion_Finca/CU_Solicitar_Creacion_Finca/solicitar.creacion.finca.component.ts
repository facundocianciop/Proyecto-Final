import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { SolicitarCreacionFincaService, Finca } from './solicitar.creacion.finca.service';

@Component({
    selector:'app-solicitar.creacion.finca',
    templateUrl: './solicitar.creacion.finca.component.html',
    styleUrls:['./solicitar.creacion.finca.component.css']
    
})

export class SolicitarCreacionFincaComponent implements OnInit{
    finca: Finca;
    constructor(private router:Router,
                private solicitarCreacionFincaService:SolicitarCreacionFincaService){

    }

    ngOnInit(){

    }
    
    apretarSolicitar(nombre:string, direccionLegal:string,ubicacion:string,tamanio:number){
        console.log("estamos aca");
        console.log("nombre: "+nombre);
        console.log("direccionLegal: "+direccionLegal);
        console.log("ubicacion: "+direccionLegal);
        console.log("tamanio: "+direccionLegal);
        //this.router.navigate(['/home']);)

        this.solicitarCreacionFincaService.solicitarCreacion(nombre,direccionLegal,ubicacion,tamanio)
                                            .then(response => this.finca=response);
        
    }

    apretarCancelar(){
        console.log("estamos aca");
        this.router.navigate(['/home']);
    }
    
}
