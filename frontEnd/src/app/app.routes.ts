import { ModuleWithProviders } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { AppComponent } from './app.component';
import { LoginComponent } from './Modulo_Seguridad/CU_Iniciar_Sesion/login.component'
import { RegistrarUsuarioComponent } from './Modulo_Seguridad/CU_Registrar_Usuario/registrar.usuario.component'
import { RecuperarCuentaComponent } from './Modulo_Seguridad/CU_Recuperar_Cuenta/recuperar.cuenta.component'

import { HomeComponent } from './Modulo_Pantallas/home.component'

import { SolicitarCreacionFincaComponent } from './Modulo_Configuracion_Finca/CU_Solicitar_Creacion_Finca/solicitar.creacion.finca.component'



// Route Configuration
export const routes: Routes = [
    { path: '', component: AppComponent },
    { path: 'login', component: LoginComponent },
    { path: 'registrar', component: RegistrarUsuarioComponent },
    { path: 'recuperarCuenta', component: RecuperarCuentaComponent },
    { path: 'home', component: HomeComponent },
    { path: 'crearFinca', component: SolicitarCreacionFincaComponent }

];

export const routing: ModuleWithProviders = RouterModule.forRoot( routes );