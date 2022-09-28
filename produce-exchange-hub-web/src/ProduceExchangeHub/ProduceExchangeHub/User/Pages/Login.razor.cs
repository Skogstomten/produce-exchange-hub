using Microsoft.AspNetCore.Components;
using Microsoft.Extensions.Localization;
using ProduceExchangeHub.Models;
using ProduceExchangeHub.Security.Abstractions;

namespace ProduceExchangeHub.User.Pages;

public partial class Login
{
    [Inject]
    private IAuthenticationManager AuthenticationManager { get; set; } = null!;
    
    [Inject]
    private NavigationManager NavigationManager { get; set; } = null!;

    [Inject]
    private IStringLocalizer<Login> Loc { get; set; } = null!;

    [Parameter, SupplyParameterFromQuery(Name = "returnUrl")]
    public string? ReturnUrl { get; set; }

    private LoginModel _loginModel = new();

    public async Task LoginEventHandler()
    {
        LoginResult result = await AuthenticationManager.LoginAsync(_loginModel.Username, _loginModel.Password);
        if (result == LoginResult.Success)
        {
            _loginModel = new LoginModel();
            NavigationManager.NavigateTo(string.IsNullOrWhiteSpace(ReturnUrl) ? "/" : ReturnUrl);
        }
    }
}