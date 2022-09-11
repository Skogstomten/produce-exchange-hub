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

        return services.AddHttpClients(settings.ApiBaseUrl)
                       .AddLocalStorage()
                       .AddAuthentication();
    }

    private static IServiceCollection AddAuthentication(this IServiceCollection services) =>
        services.AddScoped<IAuthenticationManager, OAuth2AuthenticationManager>();

    private static IServiceCollection AddLocalStorage(this IServiceCollection services) =>
        services.AddBlazoredLocalStorage()
                .AddScoped<ILocalStorage, BlazoredLocalStorageWrapper>();

    private static IServiceCollection AddHttpClients(this IServiceCollection services, string apiBaseUrl) =>
        services.AddHttpService<ICompanyService, CompanyService>("Company", apiBaseUrl)
                .AddHttpService<IAuthenticationService, AuthenticationService>("Auth", apiBaseUrl);

    private static IServiceCollection AddHttpService<TInterface, TImplementation>(
        this IServiceCollection services,
        string name,
        string apiBaseUrl
    ) where TImplementation : class, TInterface where TInterface : class
    {
        services.AddHttpClient<TInterface, TImplementation>(
            name,
            client => client.BaseAddress = new Uri(apiBaseUrl)
        );
        return services;
    }
}