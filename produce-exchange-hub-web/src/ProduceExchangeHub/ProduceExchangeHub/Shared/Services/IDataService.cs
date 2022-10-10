namespace ProduceExchangeHub.Shared.Services;

public interface IDataService
{
    Task<IEnumerable<string>> GetTimezoneNamesAsync();
}