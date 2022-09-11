namespace ProduceExchangeHub.Services;

public class AuthenticationService : ServiceBase, IAuthenticationService
{
    public AuthenticationService(HttpClient httpClient)
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