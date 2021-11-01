import { Component } from '@angular/core';
import AuthService from './services/auth-service.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  public title = 'web';
  public isLoggedIn = false;

  public constructor(
    private _authService: AuthService
  ) { }

  public loginWithGoogle() {
  }
}
