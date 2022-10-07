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

    private RegisterModel Model { get; set; } = new();

    private async Task OnRegisterUserSubmit()
    {
        await UserService.RegisterUserAsync(Model);
        Model = new RegisterModel();

        NavManager.NavigateTo("/authentication/login");
    }
}