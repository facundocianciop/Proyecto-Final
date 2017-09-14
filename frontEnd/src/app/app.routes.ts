import { ModuleWithProviders } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { AppComponent } from './app.component';
import { LoginComponent } from './Modulo_Seguridad/CU_Iniciar_Sesion/login.component'
import { RegistrarUsuarioComponent } from './Modulo_Seguridad/CU_Registrar_Usuario/registrar.usuario.component'
import { RecuperarCuentaComponent } from './Modulo_Seguridad/CU_Recuperar_Cuenta/recuperar.cuenta.component'
import { CerrarSesionComponent } from './Modulo_Seguridad/CU_Cerrar_Sesion/cerrar.sesion.component'
import { ModificarUsuarioComponent } from './Modulo_Seguridad/CU_Modificar_Usuario/modificar.usuario.component'

import { HomeFincaComponent } from './Modulo_Configuracion_Finca/Home_Finca/home.finca.component'
import { SolicitarCreacionFincaComponent } from './Modulo_Configuracion_Finca/CU_Solicitar_Creacion_Finca/solicitar.creacion.finca.component'
import { GestionarFincaComponent } from './Modulo_Configuracion_Finca/CU_Gestionar_Finca/gestionar.finca.component'



// Route Configuration
export const routes: Routes = [
    { path: '', component: AppComponent },
    { path: 'login', component: LoginComponent },
    { path: 'cerrarSesion', component: CerrarSesionComponent }, 
    { path: 'registrar', component: RegistrarUsuarioComponent },
    { path: 'recuperarCuenta', component: RecuperarCuentaComponent },
    { path: 'perfilUsuario', component: ModificarUsuarioComponent } ,
    
    { path: 'home', component: HomeFincaComponent },

    { path: 'crearFinca', component: SolicitarCreacionFincaComponent },
    { path: 'gestionarFinca', component: GestionarFincaComponent }


];

export const routing: ModuleWithProviders = RouterModule.forRoot( routes );