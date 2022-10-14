using System.Globalization;

namespace ProduceExchangeHub.Shared.Localization.Defaults;

public static class CultureDefaults
{
    public static readonly CultureInfo DefaultCulture = new("sv-SE");
    public static readonly CultureInfo[] SupportedCultures = {new("sv-SE"), new("en-GB") };

    public static CultureInfo GetBestMatch(string? culture)
    {
        if (culture == null)
            return DefaultCulture;

        if (culture.Length > 2)
            culture = culture.Substring(0, 2);

        CultureInfo? result = SupportedCultures.FirstOrDefault(
            c => c.TwoLetterISOLanguageName.Equals(culture, StringComparison.InvariantCultureIgnoreCase)
        );

        return result ?? DefaultCulture;
    }
}