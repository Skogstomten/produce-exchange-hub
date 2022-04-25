global using Microsoft.AspNetCore.Components;
global using System.Text.Json;
global using System.Text.Json.Serialization;

global using ProduceExchangeHub.Models;
global using ProduceExchangeHub.IoC;
global using ProduceExchangeHub.Common;
global using ProduceExchangeHub.Services;

using Microsoft.AspNetCore.Components.Web;
using Microsoft.AspNetCore.Components.WebAssembly.Hosting;

using ProduceExchangeHub;
using ProduceExchangeHub.Common.Authorization;

var builder = WebAssemblyHostBuilder.CreateDefault(args);
builder.RootComponents.Add<App>("#app");
builder.RootComponents.Add<HeadOutlet>("head::after");

builder.Services.AddHttpClient(
    "App",
    client => client.BaseAddress = new Uri(builder.HostEnvironment.BaseAddress)
);

builder.Services.AddScoped(sp => sp.GetRequiredService<IHttpClientFactory>().CreateClient("App"));

ApplicationSettings settings = builder.Configuration.GetSection("app").Get<ApplicationSettings>();
builder.Services.AddSingleton(_ => settings);

builder.Services.AddApplicationServices(settings);

builder.Services.AddTransient<ProduceExchangeHubAuthorizationMessageHandler>();

builder.Services.AddOidcAuthentication(options =>
{
    builder.Configuration.Bind("OidcConfiguration", options.ProviderOptions);
    builder.Configuration.Bind("UserOptions", options.UserOptions);
});

builder.Services.AddAuthorizationCore(authorizationOptions =>
{
    //authorizationOptions.AddPolicy(
    //    BethanysPieShopHRM.Shared.Policies.CanManageEmployees,
    //    BethanysPieShopHRM.Shared.Policies.CanManageEmployeesPolicy());
});

WebAssemblyHost app = builder.Build();

await app.RunAsync();