import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { LoginService, Usuario } from './login.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HomeFincaComponent } from '../../Modulo_Configuracion_Finca/Home_Finca/home.finca.component';

@Component({
    selector:'app-login',
    templateUrl: './login.component.html',
    styleUrls:['./login.component.css']
    
})

export class LoginComponent implements OnInit{
    usuarioLogeado: Usuario;
    errorMessage:string="";
    usuario:string;

    
    constructor(private router:Router,
                private loginService:LoginService){
        

    }

    ngOnInit(){

    }
    
    apretarIngresar(usuario:string,contrasenia:string){
        console.log("apretamos login");
        console.log("usuario: "+usuario);
        console.log("contasenia: "+contrasenia);
        //this.router.navigate(['/home']);)}
        this.loginService.login(usuario,contrasenia)
        .then(
            response => this.usuarioLogeado=response
        )
        .then(
            response => this.router.navigate(['/homeFinca'])
        )
        .catch(error => this.errorMessage=<any>error);
        
        
        
    
        
    }

    apretarRecuperar(){
        console.log("apretamos recuperar");
        this.router.navigate(['/recuperarCuenta']);
    }

}
