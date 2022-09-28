using ProduceExchangeHub.Security;
using ProduceExchangeHub.Security.OAuth2.Tokens;

namespace ProduceExchangeHub.Services;

public interface IAuthenticationService
{
    Task<OAuthTokens> AuthenticateAsync(string username, string password);
}