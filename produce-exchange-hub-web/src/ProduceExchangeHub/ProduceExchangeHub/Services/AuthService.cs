using System.Net.Http.Headers;
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
        FormUrlEncodedContent content = new(
            new[]
            {
                new KeyValuePair<string, string>("grant_type", "password"),
                new KeyValuePair<string, string>("username", username),
                new KeyValuePair<string, string>("password", password),
                new KeyValuePair<string, string>("scope", "profile roles")
            }
        );

        return PostAsync<OAuthTokens>(
            "token",
            content,
            new KeyValuePair<string, string>("accept", "application/json")
        );
    }
}