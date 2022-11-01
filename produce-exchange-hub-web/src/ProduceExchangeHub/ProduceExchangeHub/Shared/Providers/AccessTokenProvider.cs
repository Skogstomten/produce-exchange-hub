using ProduceExchangeHub.Shared.Models;
using ProduceExchangeHub.Shared.Services;

namespace ProduceExchangeHub.Shared.Providers;

public class AccessTokenProvider : IAccessTokenProvider
{
    private readonly ILocalStorage _localStorage;

    public AccessTokenProvider(ILocalStorage localStorage)
    {
        _localStorage = localStorage;
    }

    public async Task<string?> GetAccessTokenAsync()
    {
        OAuthTokens? oAuthTokens = await _localStorage.GetAsync<OAuthTokens>(StorageKey.OAuthTokens);
        return oAuthTokens?.AccessToken;
    }
}