import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { routing } from './app.routes';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { AppComponent } from './app.component';
import { LoginComponent } from './Modulo_Seguridad/CU_Iniciar_Sesion/login.component'
import { LoginService } from './Modulo_Seguridad/CU_Iniciar_Sesion/login.service'
import { RegistrarComponent } from './Modulo_Seguridad/CU_Registrar_Usuario/registrar.component'
import { RecuperarCuentaComponent } from './Modulo_Seguridad/CU_Recuperar_Cuenta/recuperar.cuenta.component'
import { HomeComponent } from './Modulo_Pantallas/home.component'

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    RegistrarComponent,
    RecuperarCuentaComponent,
    HomeComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    routing,
    
  ],
  providers: [LoginService],
  bootstrap: [AppComponent]
})
export class AppModule { }
