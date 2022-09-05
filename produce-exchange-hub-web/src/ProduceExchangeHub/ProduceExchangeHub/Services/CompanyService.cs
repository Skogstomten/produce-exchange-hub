using ProduceExchangeHub.Errors;

namespace ProduceExchangeHub.Services;

public class CompanyService : ICompanyService
{
    private readonly HttpClient _httpClient;

    private static readonly JsonSerializerOptions SerializerOptions = new()
        {AllowTrailingCommas = true, PropertyNameCaseInsensitive = true};

    public CompanyService(HttpClient httpClient)
    {
        _httpClient = httpClient;
    }

    public async Task<IEnumerable<CompanyListModel>> GetCompaniesAsync(
        int skip,
        int take,
        SortOrder sortOrder,
        string sortBy
    )
    {
        string GetSortOrder() => sortOrder == SortOrder.Ascending ? "asc" : "desc";
        string url = $"SV/companies/?skip={skip}&take={take}&sort_order={GetSortOrder()}&sort_by={sortBy}";
        HttpResponseMessage response = await _httpClient.GetAsync(url);
        if (response.IsSuccessStatusCode)
        {
            await using Stream stream = await response.Content.ReadAsStreamAsync();
            ListResponseModel<CompanyListModel>? listResponseModel =
                await JsonSerializer.DeserializeAsync<ListResponseModel<CompanyListModel>>(stream, SerializerOptions);
            if (listResponseModel == null)
                throw new HttpResponseMessageNullBodyException(url, response);

            return listResponseModel.Items ?? new List<CompanyListModel>();
        }

        await using Stream errorStream = await response.Content.ReadAsStreamAsync();
        ErrorModel? error = await JsonSerializer.DeserializeAsync<ErrorModel>(errorStream, SerializerOptions);
        if (error == null)
            throw new HttpResponseMessageNullBodyException(url, response);
        throw new HttpResponseException(url, error, response.StatusCode);
    }
}