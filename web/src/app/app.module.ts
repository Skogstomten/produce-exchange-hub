import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './components/home/home.component';
import CompaniesService from './services/companies.service';
import { LoginComponent } from './components/login/login.component';
import { SignUpComponent } from './components/sign-up/sign-up.component';
import AuthService from './services/auth-service.service';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    LoginComponent,
    SignUpComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
  ],
  providers: [
    { provide: 'BASE_API_URL', useFactory: getBaseUrl },
    CompaniesService,
    AuthService,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }

function getBaseUrl(): string {
  return 'http://localhost:8000/'
}