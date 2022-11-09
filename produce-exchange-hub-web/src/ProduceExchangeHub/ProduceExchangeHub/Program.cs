using Microsoft.AspNetCore.Components.Web;
using Microsoft.AspNetCore.Components.WebAssembly.Hosting;

using ProduceExchangeHub;
using ProduceExchangeHub.Admin.Extensions;
using ProduceExchangeHub.Company.Extensions;
using ProduceExchangeHub.Security.Extensions;
using ProduceExchangeHub.Shared.Extensions;
using ProduceExchangeHub.Shared.Localization.Services;
using ProduceExchangeHub.User.Extensions;

WebAssemblyHostBuilder builder = WebAssemblyHostBuilder.CreateDefault(args);
builder.RootComponents.Add<App>("#app");
builder.RootComponents.Add<HeadOutlet>("head::after");

// Application domain services
builder.Services
       .AddSharedServices(builder.Configuration)
       .AddSecurityServices(builder.Configuration)
       .AddUserServices()
       .AddCompanyServices()
       .AddAdmin();

builder.Services.AddHttpClient(
    "App",
    client => client.BaseAddress = new Uri(builder.HostEnvironment.BaseAddress)
);

builder.Services.AddLocalization();

WebAssemblyHost host = builder.Build();

// Load user culture settings on startup
await host.Services.GetRequiredService<ICultureService>().LoadCultureAsync();

await host.RunAsync();