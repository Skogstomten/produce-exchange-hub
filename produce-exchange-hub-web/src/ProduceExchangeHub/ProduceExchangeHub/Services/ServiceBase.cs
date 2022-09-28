using System.Text.Json;
using ProduceExchangeHub.Errors;
using ProduceExchangeHub.Models;

namespace ProduceExchangeHub.Services;

public class ServiceBase
{
    protected readonly HttpClient HttpClient;

    protected static readonly JsonSerializerOptions SerializerOptions = new()
        {AllowTrailingCommas = true, PropertyNameCaseInsensitive = true};

    public ServiceBase(HttpClient httpClient)
    {
        HttpClient = httpClient;
    }

    protected Task<TResponse> GetAsync<TResponse>(string uri, params KeyValuePair<string, string>[] headers) =>
        SendAsync<TResponse>(HttpMethod.Get, uri, null, headers);

    protected Task<TResponse> PostAsync<TResponse>(
        string uri,
        HttpContent content,
        params KeyValuePair<string, string>[] headers
    ) =>
        SendAsync<TResponse>(HttpMethod.Post, uri, content, headers);

    private async Task<TResponse> SendAsync<TResponse>(
        HttpMethod httpMethod,
        string uri,
        HttpContent? content,
        params KeyValuePair<string, string>[] headers
    )
    {
        HttpRequestMessage httpRequestMessage = new(httpMethod, uri);
        foreach (KeyValuePair<string, string> header in headers)
            httpRequestMessage.Headers.Add(header.Key, header.Value);
        httpRequestMessage.Content = content;

        HttpResponseMessage httpResponseMessage = await HttpClient.SendAsync(httpRequestMessage);
        if (httpResponseMessage.IsSuccessStatusCode)
        {
            await using Stream stream = await httpResponseMessage.Content.ReadAsStreamAsync();
            TResponse? response = await JsonSerializer.DeserializeAsync<TResponse>(stream, SerializerOptions);
            if (response == null)
                throw new HttpResponseMessageNullBodyException(uri, httpResponseMessage);

            return response;
        }

        await using Stream errorStream = await httpResponseMessage.Content.ReadAsStreamAsync();
        ErrorModel? error = await JsonSerializer.DeserializeAsync<ErrorModel>(errorStream, SerializerOptions);
        if (error == null)
            throw new HttpResponseMessageNullBodyException(uri, httpResponseMessage);
        throw new HttpResponseException(uri, error, httpResponseMessage.StatusCode);
    }
}