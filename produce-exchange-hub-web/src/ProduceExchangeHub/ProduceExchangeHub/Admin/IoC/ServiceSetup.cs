using ProduceExchangeHub.Admin.Services;
using ProduceExchangeHub.Shared.Extensions;

namespace ProduceExchangeHub.Admin.IoC;

public static class ServiceSetup
{
    public static IServiceCollection AddAdmin(this IServiceCollection services)
    {
        services.AddStandardHttpClient<IAdminService, AdminService>("admin");

        return services;
    }
}