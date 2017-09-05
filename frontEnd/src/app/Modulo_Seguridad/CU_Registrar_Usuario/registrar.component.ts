import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
    selector:'app-registrar',
    templateUrl: './registrar.component.html',
    styleUrls:['./registrar.component.css']
    
})

export class RegistrarComponent implements OnInit{
    errorMessage: string;
    errors: string[] = [];
    
    constructor(private router:Router){

    }

    ngOnInit(){

    }
    
    apretarRegistrar(usuario:string, contrasenia:string){
        console.log("estamos aca");
        console.log(usuario);
        console.log(contrasenia);
        //this.registrarService.login(usuario,contrasenia).then(registrar => this.router.navigate(['/']))
    }

    apretarCancelar(){
        console.log("estamos aca");
        this.router.navigate(['/']);
    }

     
}



