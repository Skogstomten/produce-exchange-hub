using Microsoft.AspNetCore.Components;
using ProduceExchangeHub.Company.Models;
using ProduceExchangeHub.Company.Services;

namespace ProduceExchangeHub.Company.Pages;

public partial class Company
{
    [Parameter]
    public string Id { get; set; } = string.Empty;

    [Inject]
    private ICompanyService CompanyService { get; set; } = null!;

    private CompanyModel Model { get; set; } = new();

    protected override async Task OnInitializedAsync()
    {
        Model = await CompanyService.GetCompanyAsync(Id);
    }
}