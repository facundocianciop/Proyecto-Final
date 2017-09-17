import { Component, OnInit, Input } from '@angular/core';
import { Router } from '@angular/router';
import { GestionarUsuarioFincaService, Usuario } from './gestionar.usuario.finca.service';

@Component({
    selector:'gestionar-usuario-finca',
    templateUrl: './gestionar.usuario.finca.component.html',
    styleUrls:['./gestionar.usuario.finca.component.css']
    
})

export class GestionarUsuarioFincaComponent implements OnInit{
    stakesFinca:Usuario[];
    
    
    
    constructor(private router:Router,
                private gestionarUsuarioFincaService:GestionarUsuarioFincaService){

    }

    ngOnInit(){
        //hay que pasar el id de la finca seleccionada
        this.gestionarUsuarioFincaService.obtenerStakeHolderFinca()
                             .then(response=>this.stakesFinca=response);
        
        
        
        /*this.homeFincaService.obtenerFincasUsuario()
                             .then(response=>this.fincasUsuario=response);
        this.homeFincaService.obtenerFincasEncargado()
                             .then(response=>this.fincasEncargado=response);*/
    }
    eliminarStakeFinca(){
        //hay que pasar el oid usuario finca
        //hay que asignarle el metodo a la imagen cuando la apretamos
        //hay que ver que devuelve para modificar la promesa
        this.gestionarUsuarioFincaService.eliminarStakeHolderFinca(1);
    }
}
