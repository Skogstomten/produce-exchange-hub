using ProduceExchangeHub.Company.Services;
using ProduceExchangeHub.Shared.Configuration;

namespace ProduceExchangeHub.Company.Extensions;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddCompanyServices(this IServiceCollection services)
    {
        services.AddHttpClient<ICompanyService, CompanyService>(
            "Company",
            (provider, client) =>
            {
                SharedSettings settings = provider.GetRequiredService<SharedSettings>();
                client.BaseAddress = new Uri(settings.ApiBaseUrl);
            }
        );

        return services;
    }
}