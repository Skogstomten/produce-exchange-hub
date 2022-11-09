using System.Text.Json.Serialization;

namespace ProduceExchangeHub.Shared.Models;

public class OAuthTokens
{
    [JsonPropertyName("access_token")]
    public string AccessToken { get; set; } = null!;
}