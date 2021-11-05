import { Component, OnInit } from '@angular/core';
import AuthService from './services/auth-service.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  public readonly title = 'web';

  public get isLoggedIn(): boolean { return this._authService.user != null; }

  public constructor(
    private _authService: AuthService
  ) { }

  public ngOnInit(): void {
    throw new Error('Method not implemented.');
  }
}
