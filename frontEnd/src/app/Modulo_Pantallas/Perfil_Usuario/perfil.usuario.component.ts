import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';



@Component({
    selector:'app-perfil-usuario',
    templateUrl: './perfil.usuario.component.html',
    styleUrls:['./perfil.usuario.component.css']
    
})

export class PerfilUsuarioComponent implements OnInit{
    editar:Boolean;
    
    constructor(private router:Router){
        this.editar=false;
    }

    ngOnInit(){

    }
    
    apretarEditar(){
        this.editar=true;       
    }

    apretarModificar(){
        console.log("estamos aca");
    }
    
    apretarCancelarModificacion(){
        this.editar=false;
    }

    apretarEliminar(){
        console.log("apretamos eliminar");
    }


}
