using ProduceExchangeHub.Admin.Services;
using ProduceExchangeHub.Shared.Extensions;

namespace ProduceExchangeHub.Admin.Extensions;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddAdmin(this IServiceCollection services)
    {
        services.AddStandardHttpClient<IAdminService, AdminService>("admin");

        return services;
    }
}