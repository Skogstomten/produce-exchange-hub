namespace ProduceExchangeHub.Shared;

public partial class NavMenu
{
    [Inject]
    private ILocalStorage LocalStorage { get; set; } = null!;

    private bool _menuOpen = false;

    private string? NavMenuCssClass => _menuOpen ? "responsive" : null;
    private string? ChangeMenuButtonClass => _menuOpen ? "change" : null;

    private bool IsLoggedIn { get; set; } = false;
    private UserInformation? UserInformation { get; set; }

    protected override async Task OnInitializedAsync()
    {
        await base.OnInitializedAsync();
        OAuthTokens? oAuthTokens = await LocalStorage.GetAsync<OAuthTokens>(StorageKey.OAuthTokens);
        if (oAuthTokens is {AccessToken: { }})
        {
            IsLoggedIn = true;
            UserInformation = await LocalStorage.GetAsync<UserInformation>(StorageKey.UserInformation);
        }
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
}