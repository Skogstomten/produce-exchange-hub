using System.Globalization;
using Microsoft.AspNetCore.Components;
using ProduceExchangeHub.Shared.Localization.Services;

namespace ProduceExchangeHub.Components;

public partial class LanguageSelector
{
    [Inject]
    private ICultureService CultureService { get; set; } = null!;

    private async Task OnLanguageSelectClick(CultureInfo cultureInfo) =>
        await CultureService.SetCultureAsync(cultureInfo);
}