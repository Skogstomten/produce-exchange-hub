namespace ProduceExchangeHub.Services;

public class CompanyService : ICompanyService
{
    private readonly ICallRestService _restService;
    
    public CompanyService(ICallRestService restService)
    {
        _restService = restService ?? throw new ArgumentNullException(nameof(restService));
    }

    public async Task<List<CompanyListModel>> GetCompaniesAsync(int skip, int take, SortOrder sortOrder, string sortBy)
    {
        string GetSortOrder() => sortOrder == SortOrder.Ascending ? "asc" : "desc";

        ListResponseModel<CompanyListModel> response = await _restService.GetAsync<ListResponseModel<CompanyListModel>>(
            $"/companies?skip={skip}&take={take}&sort_order={GetSortOrder()}&sort_by={sortBy}"
        );

        return response.Items ?? new List<CompanyListModel>();
    }
}
