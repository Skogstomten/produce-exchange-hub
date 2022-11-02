using Microsoft.AspNetCore.Components;
using Microsoft.Extensions.Localization;
using ProduceExchangeHub.Admin.Models;
using ProduceExchangeHub.Admin.Services;

namespace ProduceExchangeHub.Admin.Pages;

public partial class UserDetails
{
    [Parameter]
    public string UserId { get; set; } = string.Empty;

    [Inject]
    private IAdminService AdminService { get; set; } = null!;

    [Inject]
    private IStringLocalizer<UserDetails> Loc { get; set; } = null!;

    public UserModel User { get; set; } = new();

    protected override async Task OnInitializedAsync()
    {
        User = await AdminService.GetUserAsync(UserId);
        await base.OnInitializedAsync();
    }
}