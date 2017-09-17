import { ModuleWithProviders } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { AppComponent } from './app.component';
import { LoginComponent } from './Modulo_Seguridad/CU_Iniciar_Sesion/login.component'
import { RegistrarUsuarioComponent } from './Modulo_Seguridad/CU_Registrar_Usuario/registrar.usuario.component'
import { RecuperarCuentaComponent } from './Modulo_Seguridad/CU_Recuperar_Cuenta/recuperar.cuenta.component'
import { CerrarSesionComponent } from './Modulo_Seguridad/CU_Cerrar_Sesion/cerrar.sesion.component'
import { ModificarUsuarioComponent } from './Modulo_Seguridad/CU_Modificar_Usuario/modificar.usuario.component'

import { HomeFincaComponent } from './Modulo_Configuracion_Finca/Home_Finca/home.finca.component'
import { HomeFincaDetalleComponent } from './Modulo_Configuracion_Finca/Home_Finca_Detalle/home.finca.detalle.component'
import { SolicitarCreacionFincaComponent } from './Modulo_Configuracion_Finca/CU_Solicitar_Creacion_Finca/solicitar.creacion.finca.component'
import { GestionarFincaComponent } from './Modulo_Configuracion_Finca/CU_Gestionar_Finca/gestionar.finca.component'
import { AprobarFincaComponent } from './Modulo_Configuracion_Finca/CU_Aprobar_Finca/aprobar.finca.component'
import { GestionarUsuarioFincaComponent } from './Modulo_Configuracion_Finca/CU_Gestionar_Usuario_Finca/gestionar.usuario.finca.compontent'
import { MyComponent } from './Modulo_Configuracion_Finca/Categoria/category.component'


// Route Configuration
export const routes: Routes = [
    { path: '', component: AppComponent },
    { path: 'login', component: LoginComponent },
    { path: 'cerrarSesion', component: CerrarSesionComponent }, 
    { path: 'registrar', component: RegistrarUsuarioComponent },
    { path: 'recuperarCuenta', component: RecuperarCuentaComponent },
    { path: 'perfilUsuario', component: ModificarUsuarioComponent } ,
    
    { path: 'homeFinca', component: HomeFincaComponent },
    { path: 'homeFincaDetalle/:tamanio', component: HomeFincaDetalleComponent },
    { path: 'crearFinca', component: SolicitarCreacionFincaComponent },
    { path: 'gestionarFinca', component: GestionarFincaComponent },
    { path: 'aprobarFinca/:nombre', component: AprobarFincaComponent },
    { path: 'gestionarUsuariosFinca', component: GestionarUsuarioFincaComponent },
    { path: 'categoria', component: MyComponent }
    

    
];

export const routing: ModuleWithProviders = RouterModule.forRoot( routes );