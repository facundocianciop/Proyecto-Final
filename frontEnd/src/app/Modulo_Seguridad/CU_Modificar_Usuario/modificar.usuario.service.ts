import { Injectable } from '@angular/core';
import { Http, Headers, Response, URLSearchParams, RequestOptions } from '@angular/http';
import { RestBaseService } from '../../tools/rest.tools';
import 'rxjs/add/operator/toPromise';

@Injectable()
export class ModificarUsuarioService extends RestBaseService{
  private obtenerUsuarioActualUrl="/mostrarUsuario/"
  private modificarUrl = '/modificarUsuario/';
  private eliminarUrl = '/eliminarUsuario/';
  private modificarContraseniaUrl='/cambiarContrasenia/';

  


  constructor(private http: Http) {super();}

  obtenerUsuarioActual(): Promise<Usuario> {
    return this.http.get(ModificarUsuarioService.serverUrl + this.obtenerUsuarioActualUrl, this.getRestHeader())
    .toPromise()
    .then(response => {return response.json() as Usuario;})
    .catch(this.handleError);
  }

  modificarUsuario(usuario:string,nombre:string,apellido:string,domicilio:string,fechaNac:string,
    email:string,dni:number,cuit:number): Promise<Usuario> {
    const data = {
      'usuario': usuario,
      'nombre': nombre,
      'apellido':apellido,
      //'domicilio':domicilio,
      'fechaNacimiento':fechaNac,
      'mail':email,
      'dni':dni,
      'cuit':cuit,
      'imagenUsuario':'',
      'contraseniaNueva':'',
      'contraseniaVieja':'',
      'cookieidsesion':"ce4f5da4f01f4c92a3b2f46cda31a9b0"
    };

    return this.http.post(ModificarUsuarioService.serverUrl +this.modificarUrl, JSON.stringify(data), this.getRestHeader())
      .toPromise()
      .then(response => {
        let estado = response.status;
        return response.json() as Usuario;
        
        
      })
      .catch(this.handleError);
  }

  eliminarUsuario(id: number): Promise<Usuario> {
    if (id) {
      return this.http.delete(ModificarUsuarioService.serverUrl + this.eliminarUrl + '/' + id, this.getRestHeader())
      .toPromise()
      .then(response => {
        return response.json() as Usuario;
      })
      .catch(this.handleError);
    }
  }
  
  modificarContrasenia(passVieja:string,passNueva:string):Promise<Usuario>{
    const data = {
      'contraseniaVieja': passVieja,
      'contraseniaNueva': passNueva,
      'usuario':'ema'
    };
    return this.http.post(ModificarUsuarioService.serverUrl +this.modificarContraseniaUrl, JSON.stringify(data), this.getRestHeader())
      .toPromise()
      .then(response => {
        return response.json() as Usuario;
        
        
      })
      .catch(this.handleError);
  }
}



export interface Usuario {
  usuario;
  nombre;
  apellido;
  dni;
  cuit;

}

