using Microsoft.AspNetCore.Components;
using Microsoft.Extensions.Localization;
using ProduceExchangeHub.User.Models;

namespace ProduceExchangeHub.User.Pages;

public partial class Register
{
    [Inject]
    private IStringLocalizer<Register> Loc { get; set; } = null!;

    private RegisterModel Model { get; set; } = new();
}