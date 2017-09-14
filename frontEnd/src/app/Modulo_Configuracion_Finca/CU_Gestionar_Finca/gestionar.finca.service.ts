import { Injectable } from '@angular/core';
import { Http, Headers, Response, URLSearchParams, RequestOptions } from '@angular/http';
import { RestBaseService } from '../../tools/rest.tools';
import 'rxjs/add/operator/toPromise';

@Injectable()
export class GestionarFincaService extends RestBaseService{
  private modificarUrl="/modificarFinca/"

  constructor(private http: Http) {super();}

  modificarFinca(nombreFinca: string, dirFinca: string, ubicacionFinca:string, tamFinca:number): Promise<Finca> {
    const data = {
      'nombre': nombreFinca,
      'direccionLegal': dirFinca,
      'ubicacion':ubicacionFinca,
      'tamanio':tamFinca
    };

    return this.http.post(GestionarFincaService.serverUrl +this.modificarUrl, JSON.stringify(data), this.getRestHeader())
      .toPromise()
      .then(response => {
        return response.json() as Finca;
      })
      .catch(this.handleError);
  }

  

}

export interface Finca {
  OIDFinca: string;
  nombre: string;
  direccionLegal: string;
  ubicacion: string;
  tamanio: number;
}


