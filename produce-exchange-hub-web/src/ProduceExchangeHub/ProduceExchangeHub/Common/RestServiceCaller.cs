using System.Runtime.Serialization;

namespace ProduceExchangeHub.Common;

public class RestServiceCaller : ICallRestService
{
    private string _baseUrl;

    public RestServiceCaller(
        string baseUrl
    )
    {
        _baseUrl = baseUrl;
    }

    public async Task<T> GetAsync<T>(string url)
    {
        if (url.StartsWith("/"))
            url = url.Substring(1);

        using HttpClient client = new();

        HttpResponseMessage response = await client.GetAsync($"{_baseUrl}/{url}");
        if (response.IsSuccessStatusCode)
        {
            string bodyAsString = await response.Content.ReadAsStringAsync();
            T? body = JsonSerializer.Deserialize<T>(bodyAsString);
            if (body == null)
                throw new SerializationException(
                    $"RestServiceCaller.GetAsync(url={url}) Deserialization of body returned null: Raw='{bodyAsString}'"
                );
            return body;
        }
        throw new HttpRestException(
            response.StatusCode,
            await response.Content.ReadAsStringAsync()
        );
    }
}
