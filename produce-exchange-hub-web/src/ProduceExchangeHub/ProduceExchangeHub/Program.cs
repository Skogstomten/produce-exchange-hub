global using Microsoft.AspNetCore.Components;
global using System.Text.Json;
global using System.Text.Json.Serialization;

global using ProduceExchangeHub.Models;
global using ProduceExchangeHub.IoC;
global using ProduceExchangeHub.Common;
global using ProduceExchangeHub.Services;
global using ProduceExchangeHub.Security;

global using Blazored.LocalStorage;

using Microsoft.AspNetCore.Components.Web;
using Microsoft.AspNetCore.Components.WebAssembly.Hosting;

using ProduceExchangeHub;

WebAssemblyHostBuilder builder = WebAssemblyHostBuilder.CreateDefault(args);
builder.RootComponents.Add<App>("#app");
builder.RootComponents.Add<HeadOutlet>("head::after");

IConfiguration configuration = builder.Configuration;
ApplicationSettings settings = configuration.GetSection("App").Get<ApplicationSettings>();
builder.Services.AddSingleton(_ => settings);
builder.Services.AddApplicationServices(settings);

builder.Services.AddHttpClient(
    "App",
    client => client.BaseAddress = new Uri(builder.HostEnvironment.BaseAddress)
);

WebAssemblyHost app = builder.Build();

await app.RunAsync();