import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import {NgbModule} from '@ng-bootstrap/ng-bootstrap';
import { routing } from './app.routes';
import { FormsModule,ReactiveFormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { Ng2CompleterModule } from "ng2-completer";


import { AppComponent } from './app.component';
import { LoginComponent } from './Modulo_Seguridad/CU_Iniciar_Sesion/login.component'
import { LoginService } from './Modulo_Seguridad/CU_Iniciar_Sesion/login.service'
import { RegistrarUsuarioComponent } from './Modulo_Seguridad/CU_Registrar_Usuario/registrar.usuario.component'
import { RegistrarUsuarioService } from './Modulo_Seguridad/CU_Registrar_Usuario/registrar.usuario.service'
import { RecuperarCuentaComponent } from './Modulo_Seguridad/CU_Recuperar_Cuenta/recuperar.cuenta.component'
import { RecuperarCuentaService } from './Modulo_Seguridad/CU_Recuperar_Cuenta/recuperar.cuenta.service'
import { CerrarSesionComponent } from './Modulo_Seguridad/CU_Cerrar_Sesion/cerrar.sesion.component'
import { CerrarSesionService } from './Modulo_Seguridad/CU_Cerrar_Sesion/cerrar.sesion.service'
import { ModificarUsuarioComponent } from './Modulo_Seguridad/CU_Modificar_Usuario/modificar.usuario.component'
import { ModificarUsuarioService } from './Modulo_Seguridad/CU_Modificar_Usuario/modificar.usuario.service'

import { HomeFincaComponent } from './Modulo_Configuracion_Finca/Home_Finca/home.finca.component'
import { HomeFincaService } from './Modulo_Configuracion_Finca/Home_Finca/home.finca.service'
import { HomeFincaDetalleComponent } from './Modulo_Configuracion_Finca/Home_Finca_Detalle/home.finca.detalle.component'
import { HomeFincaDetalleService } from './Modulo_Configuracion_Finca/Home_Finca_Detalle/home.finca.detalle.service'
import { SolicitarCreacionFincaComponent } from './Modulo_Configuracion_Finca/CU_Solicitar_Creacion_Finca/solicitar.creacion.finca.component'
import { SolicitarCreacionFincaService } from './Modulo_Configuracion_Finca/CU_Solicitar_Creacion_Finca/solicitar.creacion.finca.service'
import { GestionarFincaComponent } from './Modulo_Configuracion_Finca/CU_Gestionar_Finca/gestionar.finca.component'
import { GestionarFincaService } from './Modulo_Configuracion_Finca/CU_Gestionar_Finca/gestionar.finca.service'
import { AprobarFincaComponent } from './Modulo_Configuracion_Finca/CU_Aprobar_Finca/aprobar.finca.component'
import { AprobarFincaService } from './Modulo_Configuracion_Finca/CU_Aprobar_Finca/aprobar.finca.service'
import { GestionarUsuarioFincaComponent } from './Modulo_Configuracion_Finca/CU_Gestionar_Usuario_Finca/gestionar.usuario.finca.compontent'
import { GestionarUsuarioFincaService } from './Modulo_Configuracion_Finca/CU_Gestionar_Usuario_Finca/gestionar.usuario.finca.service'
import { MyComponent } from './Modulo_Configuracion_Finca/Categoria/category.component'




@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    CerrarSesionComponent,
    RegistrarUsuarioComponent,
    RecuperarCuentaComponent,
    ModificarUsuarioComponent,

    HomeFincaComponent,
    HomeFincaDetalleComponent,
    SolicitarCreacionFincaComponent,
    GestionarFincaComponent,
    AprobarFincaComponent,
    GestionarUsuarioFincaComponent,
    MyComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    HttpModule,
    routing,
    Ng2CompleterModule,
    NgbModule.forRoot()
    
  ],
  providers: [
    LoginService,
    CerrarSesionService,
    RegistrarUsuarioService,
    RecuperarCuentaService,
    ModificarUsuarioService,

    HomeFincaService, 
    HomeFincaDetalleService,
    SolicitarCreacionFincaService,
    GestionarFincaService,
    AprobarFincaService,
    GestionarUsuarioFincaService

  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
