using ProduceExchangeHub.Security.Abstractions;
using ProduceExchangeHub.Security.OAuth2.Configuration;
using ProduceExchangeHub.Security.OAuth2.Services;
using ProduceExchangeHub.Security.Services;

namespace ProduceExchangeHub.Security.Extensions;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddSecurityServices(this IServiceCollection services, IConfiguration configuration)
    {
        OAuth2ProviderOptions options = configuration.GetSection("OAuth2").Get<OAuth2ProviderOptions>();

        services.AddSingleton(_ => options)
                .AddScoped<IAuthenticationService, AuthenticationService>()
                .AddScoped<IAuthenticationManager, OAuth2AuthenticationManager>();

        return services;
    }
}