import { Inject, Injectable } from "@angular/core";
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import IApiListResponse from "../types/api_list_response.interface";
import ICompanySmall from "../types/company_small.interface";

@Injectable({
    providedIn: 'root'
})
export default class CompaniesService {
    private readonly _apiUrl: string;

    public constructor(
        @Inject('BASE_API_URL') private readonly _baseUrl: string,
        private readonly _httpClient: HttpClient
    ) {
        this._apiUrl = _baseUrl + 'companies/';
    }

    public listCompanies(): Observable<ICompanySmall[]> {
        return this._httpClient
            .get<IApiListResponse<ICompanySmall>>(this._apiUrl)
            .pipe(
                map(value => {
                    return value.items
                })
            );
    }
}