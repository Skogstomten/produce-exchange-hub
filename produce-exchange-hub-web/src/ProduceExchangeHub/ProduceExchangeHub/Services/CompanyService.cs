using ProduceExchangeHub.Models;

namespace ProduceExchangeHub.Services;

public class CompanyService : ServiceBase, ICompanyService
{
    public CompanyService(HttpClient httpClient)
        : base(httpClient)
    {
    }

    public async Task<IEnumerable<CompanyListModel>> GetCompaniesAsync(
        int skip,
        int take,
        SortOrder sortOrder,
        string sortBy
    )
    {
        string GetSortOrder() => sortOrder == SortOrder.Ascending ? "asc" : "desc";
        string uri = $"SV/companies/?skip={skip}&take={take}&sort_order={GetSortOrder()}&sort_by={sortBy}";
        ListResponseModel<CompanyListModel> response = await GetAsync<ListResponseModel<CompanyListModel>>(uri);
        return response.Items ?? new List<CompanyListModel>();
    }
}