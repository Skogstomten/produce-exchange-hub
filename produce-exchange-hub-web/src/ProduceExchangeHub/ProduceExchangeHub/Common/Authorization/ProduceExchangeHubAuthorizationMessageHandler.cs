using Microsoft.AspNetCore.Components.WebAssembly.Authentication;

namespace ProduceExchangeHub.Common.Authorization;

public class ProduceExchangeHubAuthorizationMessageHandler : AuthorizationMessageHandler
{
    public ProduceExchangeHubAuthorizationMessageHandler(
        IAccessTokenProvider provider,
        NavigationManager navigation,
        ApplicationSettings settings
    )
        : base(provider, navigation)
    {
        ConfigureHandler(authorizedUrls: new[] { settings.ApiBaseUrl });
    }
}
