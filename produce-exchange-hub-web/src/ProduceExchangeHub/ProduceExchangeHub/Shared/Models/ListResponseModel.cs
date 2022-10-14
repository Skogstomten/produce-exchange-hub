using System.Text.Json.Serialization;

namespace ProduceExchangeHub.Shared.Models;

public class ListResponseModel<TModel>
{
    [JsonPropertyName("items")]
    public List<TModel>? Items { get; init; }
}
