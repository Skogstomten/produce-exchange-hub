using Microsoft.AspNetCore.Components.Web;
using Microsoft.AspNetCore.Components.WebAssembly.Hosting;

using ProduceExchangeHub;
using ProduceExchangeHub.IoC;
using ProduceExchangeHub.Security.Extensions;
using ProduceExchangeHub.Shared.Extensions;
using ProduceExchangeHub.Shared.Localization.Services;

WebAssemblyHostBuilder builder = WebAssemblyHostBuilder.CreateDefault(args);
builder.RootComponents.Add<App>("#app");
builder.RootComponents.Add<HeadOutlet>("head::after");

builder.Services.AddSharedServices(builder.Configuration)
       .AddSecurity(builder.Configuration)
       .AddApplicationServices();

builder.Services.AddHttpClient(
    "App",
    client => client.BaseAddress = new Uri(builder.HostEnvironment.BaseAddress)
);

builder.Services.AddLocalization();

WebAssemblyHost host = builder.Build();

await host.Services.GetRequiredService<ICultureService>().LoadCultureAsync();

await host.RunAsync();