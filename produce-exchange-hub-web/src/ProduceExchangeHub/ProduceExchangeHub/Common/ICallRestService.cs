namespace ProduceExchangeHub.Common;

public interface ICallRestService
{
    Task<T> GetAsync<T>(string url);
    Task<TResponse> PostAsync<TRequest, TResponse>(string url, TRequest request);
}
