namespace ProduceExchangeHub.IoC;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddApplicationServices(this IServiceCollection services, ApplicationSettings settings)
    {
        if (string.IsNullOrWhiteSpace(settings.ApiBaseUrl))
            throw new ApplicationException("Can't find api base url!");

        services.AddHttpClient(
            "Api",
            client => client.BaseAddress = new Uri(settings.ApiBaseUrl)
        );

        services.AddScoped(
            sp => sp
                .GetRequiredService<IHttpClientFactory>()
                .CreateClient("Api")
        );

        services
            .AddScoped<ICallRestService, RestServiceCaller>(
                
            )
            .AddScoped<ICompanyService, CompanyService>();

        return services;
    }
}
