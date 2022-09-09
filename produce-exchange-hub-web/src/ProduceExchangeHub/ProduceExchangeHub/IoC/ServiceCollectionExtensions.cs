namespace ProduceExchangeHub.IoC;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddApplicationServices(
        this IServiceCollection services,
        ApplicationSettings settings
    )
    {
        if (string.IsNullOrWhiteSpace(settings.ApiBaseUrl))
            throw new ApplicationException("Can't find api base url!");

        services.AddHttpClients(settings.ApiBaseUrl);
        services.AddLocalStorage();

        return services;
    }

    private static void AddLocalStorage(this IServiceCollection services)
    {
        services.AddBlazoredLocalStorage();
        services.AddScoped<ILocalStorage, BlazoredLocalStorageWrapper>();
    }

    private static void AddHttpClients(this IServiceCollection services, string apiBaseUrl)
    {
        services.AddHttpService<ICompanyService, CompanyService>("Company", apiBaseUrl);
        services.AddHttpService<IAuthService, AuthService>("Auth", apiBaseUrl);
    }

    private static void AddHttpService<TInterface, TImplementation>(
        this IServiceCollection services,
        string name,
        string apiBaseUrl
    ) where TImplementation : class, TInterface where TInterface : class =>
        services.AddHttpClient<TInterface, TImplementation>(name, client => client.BaseAddress = new Uri(apiBaseUrl));
}