using Blazored.LocalStorage;
using ProduceExchangeHub.Shared.Configuration;
using ProduceExchangeHub.Shared.Localization.Services;
using ProduceExchangeHub.Shared.Services;

namespace ProduceExchangeHub.Shared.Extensions;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddSharedServices(this IServiceCollection services, IConfiguration configuration)
    {
        services.AddSingleton(_ => configuration.GetSection("Shared").Get<SharedSettings>())
                .AddScoped<ICultureService, DefaultCultureService>()
                .AddScoped<ILocalStorage, BlazoredLocalStorageWrapper>()
                .AddStandardHttpClient<IDataService, DataService>("Data");

        // Third Party
        services.AddBlazoredLocalStorage();

        return services;
    }

    public static IServiceCollection AddStandardHttpClient<TInterface, TImplementation>(
        this IServiceCollection services, string name
    ) where TInterface : class where TImplementation : class, TInterface
    {
        services.AddHttpClient<TInterface, TImplementation>(
            name,
            (provider, client) => client.BaseAddress = new Uri(
                provider.GetRequiredService<SharedSettings>().ApiBaseUrl
            )
        );

        return services;
    }
}