import { Injectable } from '@angular/core';
import { Http, Headers, Response, URLSearchParams, RequestOptions } from '@angular/http';
import { RestBaseService } from '../../tools/rest.tools';
import 'rxjs/add/operator/toPromise';

@Injectable()
export class RegistrarUsuarioService extends RestBaseService{
  private loginUrl = '/registrarse/';

  


  constructor(private http: Http) {super();}

  login(username: string, password: string,email:string): Promise<Usuario> {
    const data = {
      'usuario': username,
      'contrasenia': password,
      'email':email
    };

    return this.http.put(RegistrarUsuarioService.serverUrl +this.loginUrl, JSON.stringify(data), this.getRestHeader())
      .toPromise()
      .then(response => {
        return response.json() as Usuario;
      })
      .catch(this.handleError);
  }

}

export interface Usuario {
  usuario: string;
  contrasenia: string;
  email:string;
}



