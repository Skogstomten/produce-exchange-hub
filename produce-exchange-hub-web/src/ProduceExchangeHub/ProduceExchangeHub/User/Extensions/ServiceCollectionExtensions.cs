using ProduceExchangeHub.Shared.Extensions;
using ProduceExchangeHub.User.Services;

namespace ProduceExchangeHub.User.Extensions;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddUserServices(this IServiceCollection services)
    {
        services.AddStandardHttpClient<IUserService, UserService>("User");
        return services;
    }
}