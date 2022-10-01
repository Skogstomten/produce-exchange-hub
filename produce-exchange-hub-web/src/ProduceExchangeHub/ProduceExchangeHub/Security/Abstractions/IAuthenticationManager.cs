using ProduceExchangeHub.Security.Models;
using ProduceExchangeHub.User.Models;

namespace ProduceExchangeHub.Security.Abstractions;

public interface IAuthenticationManager
{
    ValueTask<LoginResult> LoginAsync(string username, string password);
    void Subscribe(Func<AuthenticationEvent, Task> callback);
    ValueTask<UserInformation?> GetAuthenticatedUserAsync();
    ValueTask<bool> IsUserAuthenticatedAsync();
}