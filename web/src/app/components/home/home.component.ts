import { Component, OnInit } from '@angular/core';
import CompaniesService from 'src/app/services/companies.service';
import ICompanySmall from 'src/app/types/company_small.interface';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  public companies: ICompanySmall[] = []

  constructor(
    private _companiesService: CompaniesService
  ) { }

  public ngOnInit(): void {
    this._companiesService.listCompanies().subscribe(
      companies => {
        this.companies = companies;
      }
    )
  }

}
