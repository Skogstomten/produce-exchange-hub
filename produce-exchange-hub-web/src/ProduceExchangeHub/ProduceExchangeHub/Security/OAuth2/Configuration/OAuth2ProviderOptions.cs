namespace ProduceExchangeHub.Security.OAuth2.Configuration;

public class OAuth2ProviderOptions
{
    public string Scopes { get; set; } = null!;
    public string TokenEndpoint { get; set; } = null!;
    public string GrantType { get; set; } = null!;
}