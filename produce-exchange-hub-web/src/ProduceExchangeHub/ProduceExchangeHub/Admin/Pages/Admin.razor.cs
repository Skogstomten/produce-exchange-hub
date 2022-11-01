using Microsoft.AspNetCore.Components;
using Microsoft.Extensions.Localization;

namespace ProduceExchangeHub.Admin.Pages;

public partial class Admin
{
    [Inject]
    public IStringLocalizer<Admin> Loc { get; set; } = null!;
}