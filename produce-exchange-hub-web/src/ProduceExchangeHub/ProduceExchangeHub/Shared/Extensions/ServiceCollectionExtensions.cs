using ProduceExchangeHub.Shared.Configuration;
using ProduceExchangeHub.Shared.Localization.Services;

namespace ProduceExchangeHub.Shared.Extensions;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddSharedServices(this IServiceCollection services, IConfiguration configuration)
    {
        SharedSettings settings = configuration.GetSection("Shared").Get<SharedSettings>();

        services.AddSingleton(_ => settings)
                .AddScoped<ICultureService, DefaultCultureService>();

        return services;
    }
}