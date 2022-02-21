import { Component, OnInit } from '@angular/core';

import { CompaniesService } from '../../services/companies.service'
import ICompany from '../../models/company.interface'

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  public companies: ICompany[] = []


  constructor(
    private _companyService: CompaniesService
  ) { }

  public ngOnInit(): void {
    this._companyService
      .getCompaniesForStartPage()
      .subscribe(items => {
        console.log(items);
        this.companies = items;
      });
  }

}
