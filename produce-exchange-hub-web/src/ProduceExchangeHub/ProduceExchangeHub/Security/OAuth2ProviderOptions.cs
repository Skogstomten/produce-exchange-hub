namespace ProduceExchangeHub.Security;

public class OAuth2ProviderOptions
{
    public string Scopes { get; set; }
    public string TokenEndpoint { get; set; }
    public string GrantType { get; set; }
}