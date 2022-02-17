import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable, throwError } from 'rxjs'
import { catchError, retry } from 'rxjs/operators'

import IListResponse from '../models/list-response.interface';
import ICompany from '../models/company.interface'

@Injectable({
  providedIn: 'root'
})
export class CompaniesService {
  private _url: string = 'http://localhost:8000/companies'

  constructor(
    private _http: HttpClient
  ) { }

  public getCompaniesForStartPage() {
    this._http
      .get<IListResponse<ICompany>>(this._url)
      .pipe()
  }
}
