using System.Globalization;
using Microsoft.AspNetCore.Components;
using ProduceExchangeHub.Shared.Localization.Defaults;
using ProduceExchangeHub.Shared.Models;
using ProduceExchangeHub.Shared.Services;

namespace ProduceExchangeHub.Shared.Localization.Services;

public class DefaultCultureService : ICultureService
{
    private readonly ILocalStorage _localStorage;
    private readonly NavigationManager _navigationManager;

    public DefaultCultureService(ILocalStorage localStorage, NavigationManager navigationManager)
    {
        _localStorage = localStorage;
        _navigationManager = navigationManager;
    }

    public async ValueTask LoadCultureAsync()
    {
        string? result = await _localStorage.GetAsync<string>(StorageKey.BlazorCulture) ??
                         await _localStorage.GetAsync<string>("i18nextLng");

        CultureInfo culture = CultureDefaults.GetBestMatch(result);
        if (result == null)
            await _localStorage.SaveAsync(StorageKey.BlazorCulture, culture.TwoLetterISOLanguageName);

        CultureInfo.DefaultThreadCurrentCulture = culture;
        CultureInfo.DefaultThreadCurrentUICulture = culture;
    }

    public async ValueTask SetCultureAsync(CultureInfo cultureInfo)
    {
        if (!Equals(CultureInfo.CurrentCulture, cultureInfo))
        {
            await _localStorage.SaveAsync(StorageKey.BlazorCulture, cultureInfo.Name);
            _navigationManager.NavigateTo(_navigationManager.Uri, true);
        }
    }

    public ValueTask<string> GetCurrentCultureLanguageCodeISOAsync()
    {
        CultureInfo currentCulture = CultureInfo.CurrentCulture;
        return ValueTask.FromResult(currentCulture.TwoLetterISOLanguageName);
    }
}