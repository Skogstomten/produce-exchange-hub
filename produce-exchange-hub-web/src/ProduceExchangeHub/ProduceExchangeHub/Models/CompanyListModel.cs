namespace ProduceExchangeHub.Models;

public record CompanyListModel
{
    [JsonPropertyName("id")]
    public string? Id { get; init; }

    [JsonPropertyName("name")]
    public Dictionary<string, string>? Name { get; init; }

    [JsonPropertyName("status")]
    public string? Status { get; init; }

    [JsonPropertyName("created_date")]
    public DateTime? CreatedDate { get; init; }

    [JsonPropertyName("company_types")]
    public string[]? CompanyTypes { get; init; }

    [JsonPropertyName("content_languages_iso")]
    public string[]? ContentLanguagesISO { get; init; }

    [JsonPropertyName("activation_date")]
    public DateTime? ActivationDate { get; init; }

    [JsonPropertyName("description")]
    public Dictionary<string, string>? Description { get; init; }
}
