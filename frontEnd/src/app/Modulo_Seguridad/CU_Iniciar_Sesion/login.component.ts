import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { LoginService, Usuario } from './login.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
    selector:'app-login',
    templateUrl: './login.component.html',
    styleUrls:['./login.component.css']
    
})

export class LoginComponent implements OnInit{
    usuarioLogeado: Usuario;
    errorMessage:string="";
    
    constructor(private router:Router,
                private loginService:LoginService){
        

    }

    ngOnInit(){

    }
    
    apretarIngresar(usuario:string,contrasenia:string){
        console.log("apretamos login");
        console.log("usuario: "+usuario);
        console.log("contasenia: "+contrasenia);
        //this.router.navigate(['/home']);)
        this.loginService.login(usuario,contrasenia)
        .then(response => this.usuarioLogeado=response)
        .catch(error => this.errorMessage=<any>error);
        if(this.usuarioLogeado){
            this.router.navigate(['/home']);
        }
        else{
            console.log("error");
        }
        //.catch(error => this.errorMessage = <any>error);        
        
    
        
    }

    apretarRecuperar(){
        console.log("apretamos recuperar");
        this.router.navigate(['/recuperarCuenta']);
    }

}
