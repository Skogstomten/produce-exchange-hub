import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './components/home/home.component';
import CompaniesService from './services/companies.service';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [
    { provide: 'BASE_API_URL', useFactory: getBaseUrl },
    CompaniesService,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }

function getBaseUrl(): string {
  return 'http://localhost:5000/'
}