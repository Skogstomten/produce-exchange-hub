using System.Text.Json.Serialization;

namespace ProduceExchangeHub.Shared.Models;

public class ListResponseModel<TModel>
{
    [JsonPropertyName("items")]
    public TModel[]? Items { get; init; }
}
