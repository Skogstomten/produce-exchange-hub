using System.Globalization;

namespace ProduceExchangeHub.Shared.Localization.Services;

public interface ICultureService
{
    ValueTask LoadCultureAsync();
    ValueTask SetCultureAsync(CultureInfo cultureInfo);
}