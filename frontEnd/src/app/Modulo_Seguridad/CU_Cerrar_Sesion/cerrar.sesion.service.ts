import { Injectable } from '@angular/core';
import { Http, Headers, Response, URLSearchParams, RequestOptions } from '@angular/http';
import { RestBaseService } from '../../tools/rest.tools';
import 'rxjs/add/operator/toPromise';

@Injectable()
export class CerrarSesionService extends RestBaseService{
  private cerrarSesionUrl = '/finalizarSesion/';

  constructor(private http: Http) {super();}

  cerrarSesion(idsesion: string): Promise<Boolean> {
    const data = {
      'idSesion': idsesion
    };

    return this.http.post(CerrarSesionService.serverUrl +this.cerrarSesionUrl, JSON.stringify(data), this.getRestHeader())
      .toPromise()
      .then(response => {
        return response.json() as Boolean;
      })
      .catch(this.handleError);
  }

}




