using System.Text.Json.Serialization;

namespace ProduceExchangeHub.Security.OAuth2.Tokens;

public class OAuthTokens
{
    [JsonPropertyName("access_token")]
    public string AccessToken { get; set; } = null!;
}