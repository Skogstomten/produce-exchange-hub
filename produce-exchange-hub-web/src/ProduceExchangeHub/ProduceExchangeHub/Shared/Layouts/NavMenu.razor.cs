using Microsoft.AspNetCore.Components;
using ProduceExchangeHub.Models;
using ProduceExchangeHub.Services;

namespace ProduceExchangeHub.Shared.Layouts;

public partial class NavMenu
{
    [Inject]
    private IAuthenticationManager AuthenticationManager { get; set; } = null!;

    private bool _menuOpen;

    private string? NavMenuCssClass => _menuOpen ? "responsive" : null;
    private string? ChangeMenuButtonClass => _menuOpen ? "change" : null;

    private bool IsLoggedIn { get; set; }
    private UserInformation? UserInformation { get; set; }

    protected override async Task OnInitializedAsync()
    {
        AuthenticationManager.Subscribe(OnAuthenticationChangeAsync);
        bool isAuthenticated = await AuthenticationManager.IsUserAuthenticatedAsync();
        if (isAuthenticated)
            await SetAuthenticatedAsync();

        await base.OnInitializedAsync();
    }

    private void ToggleNavMenu()
    {
        _menuOpen = !_menuOpen;
    }

    private void CloseNavMeny()
    {
        if (_menuOpen)
            ToggleNavMenu();
    }

    private async Task OnAuthenticationChangeAsync(AuthenticationEvent e)
    {
        if (e.IsLoggedIn)
            await SetAuthenticatedAsync();

        StateHasChanged();
    }

    private async ValueTask SetAuthenticatedAsync()
    {
        UserInformation = await AuthenticationManager.GetAuthenticatedUserAsync();
        IsLoggedIn = true;
    }
}