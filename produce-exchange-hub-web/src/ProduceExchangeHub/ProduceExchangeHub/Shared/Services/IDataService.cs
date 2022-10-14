using ProduceExchangeHub.Shared.Models;

namespace ProduceExchangeHub.Shared.Services;

public interface IDataService
{
    Task<IEnumerable<string>> GetTimezoneNamesAsync();
    Task<IEnumerable<CountryModel>> GetCountriesAsync();
    Task<IEnumerable<LanguageModel>> GetLanguagesAsync();
}