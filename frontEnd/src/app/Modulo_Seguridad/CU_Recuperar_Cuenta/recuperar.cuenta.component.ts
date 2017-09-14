import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { RecuperarCuentaService, Cuenta } from './recuperar.cuenta.service'

@Component({
    selector:'app-recuperar',
    templateUrl: './recuperar.cuenta.component.html',
    styleUrls:['./recuperar.cuenta.component.css']
    
})

export class RecuperarCuentaComponent implements OnInit{
    divPrimero:Boolean;
    divSegundo:Boolean;
    divTercero:Boolean;
    cuenta:Cuenta;
    constructor(private router:Router,
                private recuperarCuentaService:RecuperarCuentaService){

    }

    ngOnInit(){
        this.divPrimero=true;
        this.divSegundo=false;
        this.divTercero=false;

    }

    apretarAceptarDivPrimero(email:string){
        this.recuperarCuentaService.recuperarCuenta(email).then(recuperar => this.cuenta=recuperar);
        this.divPrimero=false;
        this.divSegundo=true;        
    }

    apretarCancelarDivPrimero(){
        this.router.navigate(['/']);
    }
  
    
    apretarAceptarDivSegundo(codigo:string){
        if(this.cuenta.codigo==codigo){
            console.log("los codigos coinciden");
            this.divSegundo=false;
            this.divTercero=true;
        }
        else{
            console.log("error de codigo");
        }
    }


    apretarCancelarDivSegundo(){
        console.log("apretar cancelar div segundo");
        this.divPrimero=true;
        this.divSegundo=false;
       
    }
    apretarReestablecerDivTercero(pass1:string,pass2:string){
        if(pass1==pass2){
            console.log("los pass son iguales");
            //hay que llamar al rest de cambiar contraseña
        }
        else{
            console.log("los pass son distintos");
        }
    }
}