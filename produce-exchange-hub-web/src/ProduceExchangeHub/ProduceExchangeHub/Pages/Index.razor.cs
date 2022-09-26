using Microsoft.AspNetCore.Components;
using ProduceExchangeHub.Models;
using ProduceExchangeHub.Services;

namespace ProduceExchangeHub.Pages;

public partial class Index : ComponentBase
{
    private CompanyListModel[] Companies { get; set; } = Array.Empty<CompanyListModel>();

    [Inject]
    protected ICompanyService CompanyService { get; set; } = default!;

    protected override async Task OnInitializedAsync()
    {
        Companies = (await CompanyService.GetCompaniesAsync(0, 10, SortOrder.Descending, "created_date")).ToArray();
    }
}