import { Injectable } from '@angular/core';
import { Http, Headers, Response, URLSearchParams, RequestOptions } from '@angular/http';
import { RestBaseService } from '../../tools/rest.tools';
import 'rxjs/add/operator/toPromise';

@Injectable()
export class RecuperarCuentaService extends RestBaseService{
  private loginUrl = '/recuperarCuenta/';

  


  constructor(private http: Http) {super();}

  recuperarCuenta(email:string): Promise<Cuenta> {
    const data = {
      'email': email
    };

    return this.http.post(RecuperarCuentaService.serverUrl +this.loginUrl, JSON.stringify(data), this.getRestHeader())
      .toPromise()
      .then(response => {
        return response.json() as Cuenta;
      })
      .catch(this.handleError);
  }

}

export interface Cuenta {
  codigo:string;
  
}



