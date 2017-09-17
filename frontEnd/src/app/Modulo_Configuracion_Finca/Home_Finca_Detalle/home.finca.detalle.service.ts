import { Injectable } from '@angular/core';
import { Http, Headers, Response, URLSearchParams, RequestOptions } from '@angular/http';
import { RestBaseService } from '../../tools/rest.tools';
import 'rxjs/add/operator/toPromise';

@Injectable()
export class HomeFincaDetalleService extends RestBaseService{
  private buscarFincaUrl = '//';
  private modificarFincaUrl ="/modificarFinca/";
  


  constructor(private http: Http) {super();}

  buscarFinca(id:number):Promise<Finca> {
    return this.http.get(HomeFincaDetalleService.serverUrl + this.buscarFincaUrl, this.getRestHeader())
    .toPromise()
    .then(response => {return response.json() as Finca;})
    .catch(this.handleError);
  }

  modificarFinca(nombre:string,direccion:string,ubicacion:string,tamanio:string):Promise<Finca>{
    const data = {
      'idFinca':'',
      'nombreFinca': nombre,
      'ubicacion':ubicacion,
      'tamanio':tamanio,
      'direccionLegal':direccion,
      'logo':'',
      'nombreEstado':''
      
    };

    return this.http.post(HomeFincaDetalleService.serverUrl +this.modificarFincaUrl, JSON.stringify(data), this.getRestHeader())
      .toPromise()
      .then(response => {
        return response.json() as Finca;
        
        
      })
      .catch(this.handleError);
  }
  
}

export interface Finca {
  nombre:string;
  ubicacion:string;
  tamanio: number;
  direccionLegal:string;
  
}



