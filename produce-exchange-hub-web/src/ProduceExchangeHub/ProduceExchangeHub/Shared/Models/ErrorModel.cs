using System.Text.Json.Serialization;

namespace ProduceExchangeHub.Shared.Models;

public class ErrorModel
{
    [JsonPropertyName("detail")]
    public string? Detail { get; init; }
}