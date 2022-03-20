namespace ProduceExchangeHub.IoC;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddApplicationServices(this IServiceCollection services, ApplicationSettings settings)
    {
        services.AddSingleton<ICallRestService>(_ => new RestServiceCaller(Ensure.NotNull(settings.ApiBaseUrl)))
            .AddSingleton<ICompanyService, CompanyService>();

        return services;
    }
}
