import { Injectable } from '@angular/core';
import { Http, Headers, Response, URLSearchParams, RequestOptions } from '@angular/http';
import { RestBaseService } from '../../tools/rest.tools';
import 'rxjs/add/operator/toPromise';

@Injectable()
export class SolicitarCreacionFincaService extends RestBaseService{
  private crearFincaUrl = '/crearFinca/';
  private obtenerProvUrl = '/buscarProveedoresInformacion/';
  private selecProvUrl = '/elegirProveedorInformacion/';

  constructor(private http: Http) {super();}

  solicitarCreacion(nombreFinca: string, dirFinca: string, ubicacionFinca:string, tamFinca:number): Promise<Finca> {
    const data = {
      'nombre': nombreFinca,
      'direccionLegal': dirFinca,
      'ubicacion':ubicacionFinca,
      'tamanio':tamFinca
    };

    return this.http.post(SolicitarCreacionFincaService.serverUrl +this.crearFincaUrl, JSON.stringify(data), this.getRestHeader())
      .toPromise()
      .then(response => {
        return response.json() as Finca;
      })
      .catch(this.handleError);
  }

  obtenerProveedores():Promise<ProveedorInformacion[]>{
    return this.http.get(SolicitarCreacionFincaService.serverUrl + this.obtenerProvUrl, this.getRestHeader())
    .toPromise()
    .then(response => {return response.json() as ProveedorInformacion[];})
    .catch(this.handleError);
  }

  seleccionarProveedor(proveedor:string,oidfinca:string,oidusuario:string):Promise<any>{
    const data = {
      'nombreProveedor': proveedor,
      'OIDFinca': oidfinca,
      'OIDusuario':oidusuario

    };

    return this.http.post(SolicitarCreacionFincaService.serverUrl +this.selecProvUrl, JSON.stringify(data), this.getRestHeader())
      .toPromise()
      .then(response => {
        return "";
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

export interface ProveedorInformacion{
  nombreProveedor:string;
  frecuenciaMaxPosible:number;
  urlAPI:string;
}

