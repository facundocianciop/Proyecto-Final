import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { LoginService, Usuario } from './login.service';
import { AppComponent } from '../../app.component';

@Component({
    selector:'app-login',
    templateUrl: './login.component.html',
    styleUrls:['./login.component.css']
    
})

export class LoginComponent implements OnInit{
    usuario: Usuario;
    constructor(private router:Router,
                private loginService:LoginService){

    }

    ngOnInit(){

    }
    
    apretarIngresar(usuario:string, pass:string){
        console.log("estamos aca");
        console.log("usuario: "+usuario);
        console.log("contasenia: "+pass);
        this.router.navigate(['/home']);

        //this.loginService.login(usuario,pass).then(response => this.router.navigate['/home']);
        
        //this.router.navigate(['/home']);
    }

    apretarRecuperar(){
        console.log("estamos aca");
        this.router.navigate(['/recuperarCuenta']);
    }
    
}
