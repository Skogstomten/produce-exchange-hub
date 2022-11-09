using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Text.Json;
using ProduceExchangeHub.Shared.Exceptions;
using ProduceExchangeHub.Shared.Localization.Services;
using ProduceExchangeHub.Shared.Models;
using ProduceExchangeHub.Shared.Providers;

namespace ProduceExchangeHub.Shared.Services;

public class ServiceBase
{
    protected readonly HttpClient HttpClient;
    private readonly ICultureService _cultureService;
    private readonly ILogger _logger;
    private readonly IAccessTokenProvider _accessTokenProvider;

    protected static readonly JsonSerializerOptions SerializerOptions = new()
        {AllowTrailingCommas = true, PropertyNameCaseInsensitive = true};

    public ServiceBase(
        HttpClient httpClient,
        ICultureService cultureService,
        ILogger logger,
        IAccessTokenProvider accessTokenProvider
    )
    {
        HttpClient = httpClient;
        _cultureService = cultureService;
        _logger = logger;
        _accessTokenProvider = accessTokenProvider;
    }

    protected bool InsertLanguageCodeInURI { get; set; } = true;

    protected Task<TResponse> GetAsync<TResponse>(string uri, params KeyValuePair<string, string>[] headers) =>
        SendAsync<TResponse>(HttpMethod.Get, uri, null, headers);

    protected Task<TResponse> PostAsync<TRequestBody, TResponse>(
        string uri,
        TRequestBody requestBody,
        params KeyValuePair<string, string>[] headers
    ) => PostAsync<TResponse>(uri, JsonContent.Create(requestBody), headers);

    protected Task<TResponse> PostAsync<TResponse>(
        string uri,
        HttpContent content,
        params KeyValuePair<string, string>[] headers
    ) => SendAsync<TResponse>(HttpMethod.Post, uri, content, headers);

    protected Task<TResponse> DeleteAsync<TResponse>(string uri, params KeyValuePair<string, string>[] headers) =>
        SendAsync<TResponse>(HttpMethod.Delete, uri, null, headers);

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
            uri = $"{language.ToUpper()}/{uri}";
        }

        HttpRequestMessage httpRequestMessage = new(httpMethod, uri);
        foreach (KeyValuePair<string, string> header in headers)
            httpRequestMessage.Headers.Add(header.Key, header.Value);
        string? accessToken = await _accessTokenProvider.GetAccessTokenAsync();
        if (accessToken != null)
            httpRequestMessage.Headers.Authorization = new AuthenticationHeaderValue("Bearer", accessToken);

        httpRequestMessage.Content = content;

        HttpResponseMessage httpResponseMessage = await HttpClient.SendAsync(httpRequestMessage);
        string responseBody = await httpResponseMessage.Content.ReadAsStringAsync();
        if (httpResponseMessage.IsSuccessStatusCode)
        {
            if (typeof(TResponse) == NoResult.Value.GetType())
                return (TResponse) Convert.ChangeType(NoResult.Value, typeof(TResponse));

            TResponse? response = JsonSerializer.Deserialize<TResponse>(responseBody, SerializerOptions);
            if (response == null)
                throw new HttpResponseMessageNullBodyException(uri, httpResponseMessage, responseBody);

            return response;
        }

        try
        {
            ErrorModel? error = JsonSerializer.Deserialize<ErrorModel>(responseBody, SerializerOptions);
            if (error != null)
                throw new HttpResponseException(uri, error, httpResponseMessage.StatusCode);
        } catch (Exception ex)
        {
            _logger.LogError(ex, ex.Message);
        }

        throw new HttpResponseMessageNullBodyException(uri, httpResponseMessage, responseBody);
    }

    protected struct NoResult
    {
        public static readonly NoResult Value = new();
    }
}