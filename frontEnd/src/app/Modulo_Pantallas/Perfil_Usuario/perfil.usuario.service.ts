import { Injectable } from '@angular/core';
import { Http, Headers, Response, URLSearchParams, RequestOptions } from '@angular/http';
import { RestBaseService } from '../../tools/rest.tools';
import 'rxjs/add/operator/toPromise';

@Injectable()
export class PerfilUsuarioService extends RestBaseService{
  private loginUrl = '/mostrarUsuario/';

  


  constructor(private http: Http) {super();}


}

export interface Usuario {
  apellido:string;
  cuit:number;
  usuario: string;
  dni:number;
  nombre:string;
  email:string;
  docimicilio:string;
  fechaNacimiento;
}



