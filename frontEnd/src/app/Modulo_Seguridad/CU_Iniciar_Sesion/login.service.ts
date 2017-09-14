import { Injectable } from '@angular/core';
import { Http, Headers, Response, URLSearchParams, RequestOptions } from '@angular/http';
import { RestBaseService } from '../../tools/rest.tools';
import 'rxjs/add/operator/toPromise';

@Injectable()
export class LoginService extends RestBaseService{
  private loginUrl = '/iniciarSesion/';

  


  constructor(private http: Http) {super();}

  login(username: string, password: string): Promise<Usuario> {
    const data = {
      'usuario': username,
      'contrasenia': password,
      'tipoDispositivo':"tipoDispositivo"
    };

    return this.http.post(LoginService.serverUrl +this.loginUrl, JSON.stringify(data), this.getRestHeader())
      .toPromise()
      .then(response => {
        let estado = response.status;
        return response.json() as Usuario;

      })
      .catch(this.handleError);
  }
  
}

export interface Usuario {
  apellido:string;
  cuit:number;
  usuario: string;
  dni:number;
  OIDUsuario:string;
  nombre:string;
  email:string;
  docimicilio:string;
  fechaNacimiento;
}



