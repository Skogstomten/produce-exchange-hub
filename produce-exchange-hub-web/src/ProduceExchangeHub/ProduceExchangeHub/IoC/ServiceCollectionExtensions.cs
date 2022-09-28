using Blazored.LocalStorage;
using ProduceExchangeHub.Company.Services;
using ProduceExchangeHub.Services;
using ProduceExchangeHub.Shared.Configuration;

namespace ProduceExchangeHub.IoC;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddApplicationServices(
        this IServiceCollection services
    )
    {
        return services.AddHttpClients()
                       .AddLocalStorage()
                       .AddAuthentication();
    }
    
    private static IServiceCollection AddAuthentication(this IServiceCollection services) =>
        services.AddScoped<IAuthenticationManager, OAuth2AuthenticationManager>();

    private static IServiceCollection AddLocalStorage(this IServiceCollection services) =>
        services.AddBlazoredLocalStorage()
                .AddScoped<ILocalStorage, BlazoredLocalStorageWrapper>();

    private static IServiceCollection AddHttpClients(this IServiceCollection services) =>
        services.AddHttpService<ICompanyService, CompanyService>("Company")
                .AddHttpService<IAuthenticationService, AuthenticationService>("Auth");

    private static IServiceCollection AddHttpService<TInterface, TImplementation>(
        this IServiceCollection services,
        string name
    ) where TImplementation : class, TInterface where TInterface : class
    {
        services.AddHttpClient<TInterface, TImplementation>(
            name,
            (provider, client) =>
            {
                SharedSettings settings = provider.GetRequiredService<SharedSettings>();
                client.BaseAddress = new Uri(settings.ApiBaseUrl);
            }
        );
        return services;
    }
}