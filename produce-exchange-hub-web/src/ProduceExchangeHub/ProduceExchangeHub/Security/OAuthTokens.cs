namespace ProduceExchangeHub.Security;

public class OAuthTokens
{
    [JsonPropertyName("access_token")]
    public string Token { get; set; } = null!;

    [JsonPropertyName("token_type")]
    public string TokenType { get; set; } = null!;
}