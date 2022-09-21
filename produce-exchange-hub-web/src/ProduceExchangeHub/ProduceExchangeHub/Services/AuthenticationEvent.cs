namespace ProduceExchangeHub.Services;

public class AuthenticationEvent
{
    public AuthenticationEvent(LoginResult loginResult)
    {
        if (loginResult == LoginResult.Success)
            IsLoggedIn = true;
    }

    public bool IsLoggedIn { get; }
}