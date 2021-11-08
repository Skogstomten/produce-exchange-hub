import { Component, OnInit } from '@angular/core';
import AuthService from 'src/app/services/auth-service.service';

@Component({
  selector: 'app-nav',
  templateUrl: './nav.component.html',
  styleUrls: ['./nav.component.scss']
})
export class NavComponent implements OnInit {
  public get isLoggedIn(): boolean { return this._authService.user != null; }

  public constructor(
    private _authService: AuthService
  ) { }

  ngOnInit(): void {
  }
}
