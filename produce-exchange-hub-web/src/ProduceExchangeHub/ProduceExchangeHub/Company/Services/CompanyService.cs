using ProduceExchangeHub.Company.Models;
using ProduceExchangeHub.Shared.Localization.Services;
using ProduceExchangeHub.Shared.Models;
using ProduceExchangeHub.Shared.Providers;
using ProduceExchangeHub.Shared.Services;

namespace ProduceExchangeHub.Company.Services;

public class CompanyService : ServiceBase, ICompanyService
{
    public CompanyService(
        HttpClient httpClient,
        ICultureService cultureService,
        ILogger<CompanyService> logger,
        IAccessTokenProvider accessTokenProvider
    )
        : base(httpClient, cultureService, logger, accessTokenProvider)
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
        string uri = $"companies/?skip={skip}&take={take}&sort_order={GetSortOrder()}&sort_by={sortBy}";
        ListResponseModel<CompanyListModel> response = await GetAsync<ListResponseModel<CompanyListModel>>(uri);
        return response.Items ?? Array.Empty<CompanyListModel>();
    }

    public Task<CompanyModel> GetCompanyAsync(string id) => GetAsync<CompanyModel>($"companies/{id}/");
}