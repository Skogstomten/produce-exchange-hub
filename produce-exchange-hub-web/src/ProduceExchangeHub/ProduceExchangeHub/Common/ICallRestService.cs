namespace ProduceExchangeHub.Common;

public interface ICallRestService
{
    Task<T> GetAsync<T>(string url);
}
