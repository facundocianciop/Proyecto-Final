import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ModificarUsuarioService, Usuario} from './modificar.usuario.service'
import { FormBuilder, FormGroup, Validators } from '@angular/forms';


@Component({
    selector:'app-modificar-usuario',
    templateUrl: './modificar.usuario.component.html',
    styleUrls:['./modificar.usuario.component.css']
    
})

export class ModificarUsuarioComponent implements OnInit{
    editar:Boolean;
    userForm: any;    
    cambiarContrasenia:Boolean;
    usuarioModificado:Usuario;
    usuarioEliminado: Usuario;
    usuarioActual: Usuario;
    
    constructor(private router:Router,
                private modificarUsuarioService:ModificarUsuarioService,
                private formBuilder: FormBuilder){
        this.editar=false;
        this.cambiarContrasenia=false;
  
          
        
    }

    ngOnInit(){
        this.modificarUsuarioService.obtenerUsuarioActual()
                                    .then(response => this.usuarioActual = response);

        
    }
    
    apretarEditar(){
        this.editar=true;   
        this.cambiarContrasenia=false;    
    }

    apretarModificar(usuario:string,nombre:string,apellido:string,domicilio:string,
        fechaNac:string,email:string,dni:number,cuit:number){
        console.log("estamos aca");
        /*this.modificarUsuarioService.modificarUsuario(usuario,nombre,apellido,domicilio,fechaNac,email,dni,cuit)
        .then(response => this.usuarioModificado=response);*/
    }
    
    apretarCancelarModificacion(){
        this.editar=false;
        this.cambiarContrasenia=false;
    }

    apretarEliminar(){
        this.modificarUsuarioService.eliminarUsuario(1)
                                    .then(response => this.usuarioEliminado=response);
    }

    apretarCambiarContrasenia(){
        this.editar=false;
        this.cambiarContrasenia=true;
    }

    apretarCancelarContrasenia(){
        console.log("apretamos cancelar modificar contrasenia");
        this.router.navigate(['/perfilUsuario']);
    }
    apretarModificarContrasenia(passVieja:string,pass1:string,pass2:string){
        console.log("apretamos modificar contrasenia");
        if(pass1==pass2){
            this.modificarUsuarioService.modificarContrasenia(passVieja,pass1)
                                        .then(response => console.log(response));
        }            
        else{
            console.log("las contrasenias no coinciden");
        }                        
    }


}
