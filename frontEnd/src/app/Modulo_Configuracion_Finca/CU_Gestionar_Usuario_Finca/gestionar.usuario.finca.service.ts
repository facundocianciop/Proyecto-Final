import { Injectable } from '@angular/core';
import { Http, Headers, Response, URLSearchParams, RequestOptions } from '@angular/http';
import { RestBaseService } from '../../tools/rest.tools';
import 'rxjs/add/operator/toPromise';

@Injectable()
export class GestionarUsuarioFincaService extends RestBaseService{
  private buscarStakeFincaUrl = '/buscarStakeholdersFinca/';
  private eliminarStakeFincaUrl = '/obtenerFincasPorUsuario/';
  private buscarUsuarioUrl = '/buscarUsuarios/';
  private agregarUsaurioUrl = '/agregarUsuarioFinca/';
  private modificarRolUsuarioUrl="/modificarRolUsuario/"


  constructor(private http: Http) {super();}

  obtenerStakeHolderFinca():Promise<Usuario[]> {
      const data = {
          'idFinca': ''
          
      };

      return this.http.post(GestionarUsuarioFincaService.serverUrl + this.buscarStakeFincaUrl, JSON.stringify(data), this.getRestHeader())
          .toPromise()
          .then(response => {
              return response.json() as Usuario[];


          })
          .catch(this.handleError);
    }

    eliminarStakeHolderFinca(id: number): Promise<Usuario> {
        if (id) {
          return this.http.delete(GestionarUsuarioFincaService.serverUrl + this.eliminarStakeFincaUrl + '/' + id, this.getRestHeader())
          .toPromise()
          .then(response => {
            return response.json() as Usuario;
          })
          .catch(this.handleError);
        }
    }

    buscarUsuarios(){
      return this.http.get(GestionarUsuarioFincaService.serverUrl + this.buscarUsuarioUrl, this.getRestHeader())
      .toPromise()
      .then(response => {return response.json() as Usuario[];})
      .catch(this.handleError);
    }

    agregarUsuarioFinca(oidFinca: string, oidUsaurio: string,rol:string): Promise<any> {
      const data = {
        'OIDFinca': oidFinca,
        'OIDUsuario': oidUsaurio,
        'nombreRol':rol
      };
  
      return this.http.put(GestionarUsuarioFincaService.serverUrl +this.agregarUsaurioUrl, JSON.stringify(data), this.getRestHeader())
        .toPromise()
        .then(response => {
          return response.json() as any;
        })
        .catch(this.handleError);
    }

    modificarRolUsuario(oidUsuario:string,rol:string):Promise<any> {
      const data = {
          'OIDUsuario': oidUsuario,
          'nombreRol':rol
          
      };

      return this.http.post(GestionarUsuarioFincaService.serverUrl + this.modificarRolUsuarioUrl, JSON.stringify(data), this.getRestHeader())
          .toPromise()
          .then(response => {
              return response.json() as any;


          })
          .catch(this.handleError);
    }
}

export interface Usuario {
  OIDUsuarioFinca:string;
  nombreUsuario:string;
  apellidoUsuario: string;
  email:string;
  imagenUsuario;
  rol:string;
  
}




