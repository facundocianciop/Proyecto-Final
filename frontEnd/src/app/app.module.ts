import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import {NgbModule} from '@ng-bootstrap/ng-bootstrap';
import { routing } from './app.routes';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { AppComponent } from './app.component';
import { LoginComponent } from './Modulo_Seguridad/CU_Iniciar_Sesion/login.component'
import { LoginService } from './Modulo_Seguridad/CU_Iniciar_Sesion/login.service'
import { RegistrarUsuarioComponent } from './Modulo_Seguridad/CU_Registrar_Usuario/registrar.usuario.component'
import { RegistrarUsuarioService } from './Modulo_Seguridad/CU_Registrar_Usuario/registrar.usuario.service'
import { RecuperarCuentaComponent } from './Modulo_Seguridad/CU_Recuperar_Cuenta/recuperar.cuenta.component'


import { HomeComponent } from './Modulo_Pantallas/home.component'

import { SolicitarCreacionFincaComponent } from './Modulo_Configuracion_Finca/CU_Solicitar_Creacion_Finca/solicitar.creacion.finca.component'
import { SolicitarCreacionFincaService } from './Modulo_Configuracion_Finca/CU_Solicitar_Creacion_Finca/solicitar.creacion.finca.service'


@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    RegistrarUsuarioComponent,
    RecuperarCuentaComponent,
    HomeComponent,
    SolicitarCreacionFincaComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    routing,
    NgbModule.forRoot()
    
  ],
  providers: [LoginService,SolicitarCreacionFincaService,RegistrarUsuarioService],
  bootstrap: [AppComponent]
})
export class AppModule { }
