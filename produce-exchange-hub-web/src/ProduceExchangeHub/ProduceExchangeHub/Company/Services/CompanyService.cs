using ProduceExchangeHub.Models;
using ProduceExchangeHub.Services;
using ProduceExchangeHub.Shared.Localization.Services;

namespace ProduceExchangeHub.Company.Services;

public class CompanyService : ServiceBase, ICompanyService
{
    private readonly ICultureService _cultureService;

    public CompanyService(HttpClient httpClient, ICultureService cultureService)
        : base(httpClient)
    {
        _cultureService = cultureService;
    }

    public async Task<IEnumerable<CompanyListModel>> GetCompaniesAsync(
        int skip,
        int take,
        SortOrder sortOrder,
        string sortBy
    )
    {
        string language = await _cultureService.GetCurrentCultureLanguageCodeISOAsync();
        string GetSortOrder() => sortOrder == SortOrder.Ascending ? "asc" : "desc";
        string uri = $"{language.ToUpper()}/companies/?skip={skip}&take={take}&sort_order={GetSortOrder()}&sort_by={sortBy}";
        ListResponseModel<CompanyListModel> response = await GetAsync<ListResponseModel<CompanyListModel>>(uri);
        return response.Items ?? new List<CompanyListModel>();
    }
}