import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import ListResponse from '../models/ListResponse.interface';
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
    this._http.get<ListResponse<ICompany>>(this._url)
  }
}
