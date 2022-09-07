using ProduceExchangeHub.Security;

namespace ProduceExchangeHub.Services;

public class AuthService : ServiceBase, IAuthService
{
    public AuthService(HttpClient httpClient)
        : base(httpClient)
    {
    }

    public Task<OAuthTokens> AuthenticateAsync(string username, string password)
    {
        return PostAsync<OAuthTokens>(
            "/token",
            new FormUrlEncodedContent(
                new[]
                {
                    new KeyValuePair<string, string>("grant_type", "password"),
                    new KeyValuePair<string, string>("username", username),
                    new KeyValuePair<string, string>("password", password),
                    new KeyValuePair<string, string>("scope", "profile roles")
                }
            ),
            new KeyValuePair<string, string>("accept", "application/json"),
            new KeyValuePair<string, string>("Content-Type", "application/x-www-form-urlencoded")
        );
    }
}