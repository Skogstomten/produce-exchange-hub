using Microsoft.AspNetCore.Components;
using Microsoft.Extensions.Localization;
using ProduceExchangeHub.Admin.Models;
using ProduceExchangeHub.Admin.Services;
using ProduceExchangeHub.Shared.Models;

namespace ProduceExchangeHub.Admin.Components;

public partial class UsersComponent
{
    [Inject]
    private IStringLocalizer<UsersComponent> Loc { get; set; } = null!;

    [Inject]
    private IAdminService AdminService { get; set; } = null!;

    [Inject]
    private NavigationManager NavManager { get; set; } = null!;

    private UserModel[] Users { get; set; } = Array.Empty<UserModel>();

    protected override async Task OnInitializedAsync()
    {
        ListResponseModel<UserModel> usersResponse = await AdminService.GetUsersAsync();
        if (usersResponse.Items != null)
            Users = usersResponse.Items;

        await base.OnInitializedAsync();
    }

    private void GoToUser(string userId) => NavManager.NavigateTo($"/user/{userId}");
}