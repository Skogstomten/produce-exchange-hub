namespace ProduceExchangeHub.Pages;

public partial class Login
{
    [Inject]
    private IAuthService AuthService { get; set; } = null!;

    private LoginModel _loginModel = new();

    public async Task LoginEventHandler()
    {
        OAuthTokens oAuthTokens = await AuthService.AuthenticateAsync(_loginModel.Username, _loginModel.Password);
    }
}
