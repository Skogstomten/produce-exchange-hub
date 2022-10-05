using ProduceExchangeHub.Company.Services;
using ProduceExchangeHub.Shared.Extensions;

namespace ProduceExchangeHub.Company.Extensions;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddCompanyServices(this IServiceCollection services)
    {
        services.AddStandardHttpClient<ICompanyService, CompanyService>("Company");

        return services;
    }
}