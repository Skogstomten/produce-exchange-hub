using ProduceExchangeHub.Security.OAuth2.Tokens;

namespace ProduceExchangeHub.Security.Services;

public interface IAuthenticationService
{
    Task<OAuthTokens> AuthenticateAsync(string username, string password);
}