import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import {RegistrarUsuarioService, Usuario} from './registrar.usuario.service'

@Component({
    selector:'app-registrar',
    templateUrl: './registrar.usuario.component.html',
    styleUrls:['./registrar.usuario.component.css']
    
})

export class RegistrarUsuarioComponent implements OnInit{
    errorMessage: string;
    errors: string[] = [];
    usuarioRegistrado: Usuario;
    
    constructor(private router:Router,
                private registrarUsuarioService:RegistrarUsuarioService){

    }

    ngOnInit(){

    }
    
    apretarRegistrar(usuario:string, contrasenia:string,email:string){
        console.log("estamos aca");
        console.log(usuario);
        console.log(contrasenia);
        console.log(email);
        //this.router.navigate(['/login']);
        this.registrarUsuarioService.login(usuario,contrasenia,email).then(registrar => this.usuarioRegistrado=registrar);
    }

    apretarCancelar(){
        console.log("estamos aca");
        this.router.navigate(['/']);
    }

     
}



