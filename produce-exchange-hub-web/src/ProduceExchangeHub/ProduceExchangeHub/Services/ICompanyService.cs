namespace ProduceExchangeHub.Services;

public interface ICompanyService
{
    Task<IEnumerable<CompanyListModel>> GetCompaniesAsync(int skip, int take, SortOrder sortOrder, string sortBy);
}
