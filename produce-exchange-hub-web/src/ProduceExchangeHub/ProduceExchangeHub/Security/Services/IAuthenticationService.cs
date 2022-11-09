using ProduceExchangeHub.Shared.Models;

namespace ProduceExchangeHub.Security.Services;

public interface IAuthenticationService
{
    Task<OAuthTokens> AuthenticateAsync(string username, string password);
}