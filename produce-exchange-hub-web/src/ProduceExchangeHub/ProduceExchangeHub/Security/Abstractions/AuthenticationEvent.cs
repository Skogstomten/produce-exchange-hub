using ProduceExchangeHub.User.Models;

namespace ProduceExchangeHub.Security.Abstractions;

public class AuthenticationEvent
{
    public AuthenticationEvent(LoginResult loginResult)
    {
        if (loginResult == LoginResult.Success)
            IsLoggedIn = true;
    }

    public bool IsLoggedIn { get; }
}