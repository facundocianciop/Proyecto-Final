import { ModuleWithProviders } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { AppComponent } from './app.component';
import { LoginComponent } from './Modulo_Seguridad/CU_Iniciar_Sesion/login.component'
import { RegistrarComponent } from './Modulo_Seguridad/CU_Registrar_Usuario/registrar.component'
import { RecuperarCuentaComponent } from './Modulo_Seguridad/CU_Recuperar_Cuenta/recuperar.cuenta.component'
import { HomeComponent } from './Modulo_Pantallas/home.component'



// Route Configuration
export const routes: Routes = [
    { path: '', component: AppComponent },
    { path: 'login', component: LoginComponent },
    { path: 'registrar', component: RegistrarComponent },
    { path: 'recuperarCuenta', component: RecuperarCuentaComponent },
    { path: 'home', component: HomeComponent }
    

];

export const routing: ModuleWithProviders = RouterModule.forRoot( routes );