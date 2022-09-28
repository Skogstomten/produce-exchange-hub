using System.Globalization;
using Microsoft.AspNetCore.Components;
using ProduceExchangeHub.Models;
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
        CultureInfo culture;
        string? result = await _localStorage.GetAsync<string>(StorageKey.BlazorCulture) ??
                         await _localStorage.GetAsync<string>("i18nextLng");

        if (result != null)
        {
            if (result == "en-US")
                result = "en-GB";
            culture = new CultureInfo(result);
        } else
        {
            culture = new CultureInfo("sv-SE");
            await _localStorage.SaveAsync(StorageKey.BlazorCulture, "sv-SE");
        }

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