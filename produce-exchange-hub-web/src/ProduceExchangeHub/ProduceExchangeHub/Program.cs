global using Microsoft.AspNetCore.Components;
global using System.Text.Json;
global using System.Text.Json.Serialization;

global using ProduceExchangeHub.Models;
global using ProduceExchangeHub.IoC;
global using ProduceExchangeHub.Common;
global using ProduceExchangeHub.Common.Authorization;
global using ProduceExchangeHub.Services;

using Microsoft.AspNetCore.Components.Web;
using Microsoft.AspNetCore.Components.WebAssembly.Hosting;
using Microsoft.AspNetCore.Components.WebAssembly.Authentication;

using ProduceExchangeHub;

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

await builder.Build().RunAsync();
