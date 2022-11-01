using ProduceExchangeHub.Shared.Localization.Services;
using ProduceExchangeHub.Shared.Models;
using ProduceExchangeHub.Shared.Providers;

namespace ProduceExchangeHub.Shared.Services;

public class DataService : ServiceBase, IDataService
{
    public DataService(
        HttpClient httpClient,
        ICultureService cultureService,
        ILogger<DataService> logger,
        IAccessTokenProvider accessTokenProvider
    )
        : base(httpClient, cultureService, logger, accessTokenProvider)
    {
    }

    public async Task<IEnumerable<string>> GetTimezoneNamesAsync()
    {
        string[] timezoneNames = await GetAsync<string[]>("timezones/");
        return timezoneNames;
    }

    public async Task<IEnumerable<CountryModel>> GetCountriesAsync()
    {
        CountryModel[] countries = await GetAsync<CountryModel[]>("countries/");
        return countries;
    }

    public async Task<IEnumerable<LanguageModel>> GetLanguagesAsync()
    {
        LanguageModel[] languages = await GetAsync<LanguageModel[]>("languages/");
        return languages;
    }
}