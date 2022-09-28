using ProduceExchangeHub.Security.OAuth2.Configuration;

namespace ProduceExchangeHub.Security.Extensions;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddSecurity(this IServiceCollection services, IConfiguration configuration)
    {
        OAuth2ProviderOptions options = configuration.GetSection("OAuth2").Get<OAuth2ProviderOptions>();

        services.AddSingleton(_ => options);

        return services;
    }
}