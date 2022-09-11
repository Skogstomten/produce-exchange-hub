using ProduceExchangeHub.Security;

namespace ProduceExchangeHub.Services;

public interface IAuthenticationService
{
    Task<OAuthTokens> AuthenticateAsync(string username, string password);
}