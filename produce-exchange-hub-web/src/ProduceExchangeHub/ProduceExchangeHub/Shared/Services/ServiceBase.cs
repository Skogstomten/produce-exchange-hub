using System.Net.Http.Json;
using System.Text.Json;
using ProduceExchangeHub.Shared.Exceptions;
using ProduceExchangeHub.Shared.Localization.Services;
using ProduceExchangeHub.Shared.Models;

namespace ProduceExchangeHub.Shared.Services;

public class ServiceBase
{
    protected readonly HttpClient HttpClient;
    private readonly ICultureService _cultureService;

    protected static readonly JsonSerializerOptions SerializerOptions = new()
        {AllowTrailingCommas = true, PropertyNameCaseInsensitive = true};

    public ServiceBase(HttpClient httpClient, ICultureService cultureService)
    {
        HttpClient = httpClient;
        _cultureService = cultureService;
    }

    protected bool InsertLanguageCodeInURI { get; set; } = true;

    protected Task<TResponse> GetAsync<TResponse>(string uri, params KeyValuePair<string, string>[] headers) =>
        SendAsync<TResponse>(HttpMethod.Get, uri, null, headers);

    protected Task<TResponse> PostAsync<TRequestBody, TResponse>(
        string uri,
        TRequestBody requestBody,
        params KeyValuePair<string, string>[] headers
    )
        where TRequestBody : class where TResponse : class
        => PostAsync<TResponse>(uri, JsonContent.Create(requestBody), headers);

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
        if (InsertLanguageCodeInURI)
        {
            string language = await _cultureService.GetCurrentCultureLanguageCodeISOAsync();
            uri = $"{language}/{uri}";
        }
            
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