using System.Text.Json.Serialization;

namespace ProduceExchangeHub.Models;

public class ErrorModel
{
    [JsonPropertyName("detail")]
    public string? Detail { get; init; }
}