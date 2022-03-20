namespace ProduceExchangeHub.Common;

public static class Ensure
{
    public static string NotNull(string? value)
    {
        if (value == null)
            throw new ArgumentNullException("value");
        return value;
    }
}
