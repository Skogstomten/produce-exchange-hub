export default interface ICompany {
    id: string;
    content_languages_iso: string[];
    company_types_localized: string[];
    created_date: Date;
    name_localized: string;
    description_localized: string;
    status: string;
    status_localized: string;
    picture_url: string;
}