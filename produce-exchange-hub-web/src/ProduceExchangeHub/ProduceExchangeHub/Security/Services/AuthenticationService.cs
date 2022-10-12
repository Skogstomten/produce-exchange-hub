using ProduceExchangeHub.Security.OAuth2.Configuration;
using ProduceExchangeHub.Security.OAuth2.Tokens;
using ProduceExchangeHub.Shared.Localization.Services;
using ProduceExchangeHub.Shared.Services;

namespace ProduceExchangeHub.Security.Services;

public class AuthenticationService : ServiceBase, IAuthenticationService
{
    private readonly OAuth2ProviderOptions _providerOptions;

    public AuthenticationService(
        HttpClient httpClient,
        OAuth2ProviderOptions providerOptions,
        ICultureService cultureService,
        ILogger<AuthenticationService> logger
    )
        : base(httpClient, cultureService, logger)
    {
        _providerOptions = providerOptions;
        InsertLanguageCodeInURI = false;
    }

    public Task<OAuthTokens> AuthenticateAsync(string username, string password)
    {
        FormUrlEncodedContent content = new(
            new[]
            {
                new KeyValuePair<string, string>("grant_type", _providerOptions.GrantType),
                new KeyValuePair<string, string>("username", username),
                new KeyValuePair<string, string>("password", password),
                new KeyValuePair<string, string>("scope", _providerOptions.Scopes)
            }
        );

        return PostAsync<OAuthTokens>(
            _providerOptions.TokenEndpoint,
            content,
            new KeyValuePair<string, string>("accept", "application/json")
        );
    }
}