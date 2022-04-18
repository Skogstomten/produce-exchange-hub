using Microsoft.AspNetCore.Components.WebAssembly.Authentication;

namespace ProduceExchangeHub.Common.Authorization;

public class OAuth2UsernamePasswordAuthorizationMessageHandler : AuthorizationMessageHandler
{
    public OAuth2UsernamePasswordAuthorizationMessageHandler(
        IAccessTokenProvider provider,
        NavigationManager navigation,
        ApplicationSettings settings
    )
        : base(provider, navigation)
    {
        ConfigureHandler(
            authorizedUrls: new[] { settings.ApiBaseUrl }
        );
    }
}
