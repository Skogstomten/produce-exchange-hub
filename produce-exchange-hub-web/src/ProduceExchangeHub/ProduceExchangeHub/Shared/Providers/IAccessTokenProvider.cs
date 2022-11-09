namespace ProduceExchangeHub.Shared.Providers;

public interface IAccessTokenProvider
{
    Task<string?> GetAccessTokenAsync();
}