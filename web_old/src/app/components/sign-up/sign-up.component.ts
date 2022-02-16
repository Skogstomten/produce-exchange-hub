import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import AuthService from 'src/app/services/auth-service.service';

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.scss']
})
export class SignUpComponent implements OnInit {
  registerForm: FormControl = new FormControl('');

  constructor(
    private _authService: AuthService
  ) { }

  ngOnInit(): void {
  }

  public registerUser(email: string, password: string): void {
    this._authService.createUserWithUsernameAndPassword(email, password)
      .subscribe(
        next => {
          alert('User Created! ' + next.user.email)
        },
        error => {
          console.log(error)
        }
      )
  }
}
