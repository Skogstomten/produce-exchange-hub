namespace ProduceExchangeHub.Services;

public interface ICompanyService
{
    Task<List<CompanyListModel>> GetCompaniesAsync(int skip, int take, SortOrder sortOrder, string sortBy);
}
