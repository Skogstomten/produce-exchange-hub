using Microsoft.AspNetCore.Components;
using Microsoft.Extensions.Localization;
using ProduceExchangeHub.User.Models;
using ProduceExchangeHub.User.Services;

namespace ProduceExchangeHub.User.Pages;

public partial class Register
{
    [Inject]
    private IStringLocalizer<Register> Loc { get; set; } = null!;

    [Inject]
    private IUserService UserService { get; set; } = null!;

    [Inject]
    private NavigationManager NavManager { get; set; } = null!;

    private RegisterModel Model { get; set; } = new() {Country = "SE"};

    private string? Message { get; set; }

    private async Task OnRegisterUserSubmit()
    {
        Message = null;
        if (Model.Password != Model.ConfirmPassword)
        {
            Message = Loc["PasswordsNotMatchingMessage"];
            return;
        }

        await UserService.RegisterUserAsync(Model);
        Model = new RegisterModel();

        NavManager.NavigateTo("/authentication/login");
    }
}