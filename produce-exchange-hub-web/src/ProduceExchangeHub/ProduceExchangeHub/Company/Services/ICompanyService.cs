using ProduceExchangeHub.Models;

namespace ProduceExchangeHub.Company.Services;

public interface ICompanyService
{
    Task<IEnumerable<CompanyListModel>> GetCompaniesAsync(int skip, int take, SortOrder sortOrder, string sortBy);
}
