import { Component, OnInit } from '@angular/core';
import CompaniesService from 'src/app/services/companies.service';
import ICompany from 'src/app/types/company.interface';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  public companies: ICompany[] = []

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
