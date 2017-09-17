import { Injectable } from '@angular/core';
import { Http, Headers, Response, URLSearchParams, RequestOptions } from '@angular/http';
import { RestBaseService } from '../../tools/rest.tools';
import 'rxjs/add/operator/toPromise';

@Injectable()
export class RecuperarCuentaService extends RestBaseService{
  private recuerparUrl = '/recuperarCuenta/';

  


  constructor(private http: Http) {super();}

  recuperarCuenta(email:string) {
    const data = {
      'email': email
    };

    return this.http.post(RecuperarCuentaService.serverUrl +this.recuerparUrl, JSON.stringify(data), this.getRestHeader())
      .toPromise()
      .then(response => {
        return response.json();
      })
      .catch(this.handleError);
  }

}

export interface Cuenta {
  codigo:string;
  
}



