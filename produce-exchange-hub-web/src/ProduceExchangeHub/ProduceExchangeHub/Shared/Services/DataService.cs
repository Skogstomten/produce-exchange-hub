using ProduceExchangeHub.Shared.Localization.Services;

namespace ProduceExchangeHub.Shared.Services;

public class DataService : ServiceBase, IDataService
{
    public DataService(HttpClient httpClient, ICultureService cultureService)
        : base(httpClient, cultureService)
    {
    }

    public async Task<IEnumerable<string>> GetTimezoneNamesAsync()
    {
        string[] timezoneNames = await GetAsync<string[]>("timezones/");
        return timezoneNames;
    }
}