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

var builder = WebAssemblyHostBuilder.CreateDefault(args);
builder.RootComponents.Add<App>("#app");
builder.RootComponents.Add<HeadOutlet>("head::after");

var http = new HttpClient()
{
    BaseAddress = new Uri(builder.HostEnvironment.BaseAddress)
};

builder.Services.AddScoped(sp => http);

ApplicationSettings settings = builder.Configuration.GetSection("app").Get<ApplicationSettings>();

builder.Services.AddApplicationServices(settings);

await builder.Build().RunAsync();
