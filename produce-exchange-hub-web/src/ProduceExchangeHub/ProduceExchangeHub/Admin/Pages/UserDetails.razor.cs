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

    [Inject]
    private NavigationManager NavManager { get; set; } = null!;

    public UserModel User { get; set; } = new();
    private bool ShowConfirmDeleteUser { get; set; }

    protected override async Task OnInitializedAsync()
    {
        ShowConfirmDeleteUser = false;
        User = await AdminService.GetUserAsync(UserId);
        await base.OnInitializedAsync();
    }

    #region Event handlers

    private void OnDeleteUserClicked()
    {
        ShowConfirmDeleteUser = true;
        StateHasChanged();
    }

    private async Task OnDeleteUserConfirm()
    {
        await AdminService.DeleteUserAsync(User.Id);
        NavManager.NavigateTo("/admin");
    }

    private void OnDeleteUserCancel()
    {
        ShowConfirmDeleteUser = false;
        StateHasChanged();
    }

    #endregion Event handlers
}