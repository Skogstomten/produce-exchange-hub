using System.Security.Claims;

namespace ProduceExchangeHub.Pages;

public partial class Login
{
    [Inject]
    private IAuthService AuthService { get; set; } = null!;

    [Inject]
    private ILocalStorage LocalStorage { get; set; } = null!;

    [Inject]
    private NavigationManager NavigationManager { get; set; } = null!;

    [Parameter, SupplyParameterFromQuery(Name = "returnUrl")]
    public string? ReturnUrl { get; set; }

    private LoginModel _loginModel = new();

    public async Task LoginEventHandler()
    {
        OAuthTokens oAuthTokens = await AuthService.AuthenticateAsync(_loginModel.Username, _loginModel.Password);

        IEnumerable<Claim> claims = JwtHelper.DecodeJwtToken(oAuthTokens.AccessToken);
        string? email = null, firstName = null, lastName = null, id = null;
        bool verified = false;
        List<string> roles = new();
        foreach (Claim claim in claims)
            switch (claim.Type)
            {
                case "email":
                    email = claim.Value;
                    break;
                case "given_name":
                    firstName = claim.Value;
                    break;
                case "family_name":
                    lastName = claim.Value;
                    break;
                case "id":
                    id = claim.Value;
                    break;
                case "verified":
                    verified = bool.Parse(claim.Value);
                    break;
                case "roles":
                    roles.Add(claim.Value);
                    break;
            }

        UserInformation userInformation = new(id, firstName, lastName, email, verified, roles);

        await LocalStorage.SaveAsync(StorageKeys.OAuthTokens, oAuthTokens);
        await LocalStorage.SaveAsync(StorageKeys.UserInformation, userInformation);

        _loginModel = new LoginModel();
        NavigationManager.NavigateTo(string.IsNullOrWhiteSpace(ReturnUrl) ? "/" : ReturnUrl);
    }
}