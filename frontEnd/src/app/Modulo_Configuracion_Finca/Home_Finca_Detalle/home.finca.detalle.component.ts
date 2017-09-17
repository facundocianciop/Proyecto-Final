import { Component, OnInit, Input } from '@angular/core';
import { Router } from '@angular/router';
import { ActivatedRoute } from '@angular/router';
import { HomeFincaDetalleService,Finca } from './home.finca.detalle.service';

@Component({
    selector:'homeFincaDetalle',
    templateUrl: './home.finca.detalle.component.html',
    styleUrls:['./home.finca.detalle.component.css']
    
})

export class HomeFincaDetalleComponent implements OnInit{
    //fincaEncontrada=Finca;
    //fincaModificada=Finca;
    editar:Boolean;

    
    constructor(private router:Router,
                private route:ActivatedRoute,
                private homeFincaDetalleService:HomeFincaDetalleService){
        this.route.params.subscribe(params => {
        let tamanio = +params['tamanio'];
        console.log("tamanio: "+tamanio);
        /*if (tamanio) {
            this.homeFincaDetalleService.buscarFinca(id)
                                        .then(finca => this.fincaEncontrada = finca);
        }*/

        });

    }

    ngOnInit(){
        this.editar=false;
    
    }

    apretarEditarFinca(){
        this.editar=true;
        //se deberian setear los valores acutales de la finca, hay que usar fincaEncontrada
    }
    apretarEliminarFinca(){
        //falta rest eliminar Finca
        //this.homeFincaDetalleService.eliminarFinca(1);
    }
    apretarAceptarModificacionFinca(nombre:string,direccion:string,ubicacion:string,tamanio:number){
        this.editar=false;
        /*this.homeFincaDetalleService.modificarFinca(nombre,direccion,ubicacion,tamanio)
                                    .then(response=this.fincaModificada=response);*/
    }
    apretarCancelarModificacion(){
        this.editar=false;
    }

    apretarAdministrarUsuario(){
        this.router.navigate(['/gestionarUsuariosFinca']);
        //deberia pasar el id de la finca 
    }
}
