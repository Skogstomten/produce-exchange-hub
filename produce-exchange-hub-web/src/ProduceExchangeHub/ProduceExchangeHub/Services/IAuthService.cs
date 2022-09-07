using ProduceExchangeHub.Security;

namespace ProduceExchangeHub.Services;

public interface IAuthService
{
    Task<OAuthTokens> AuthenticateAsync(string username, string password);
}