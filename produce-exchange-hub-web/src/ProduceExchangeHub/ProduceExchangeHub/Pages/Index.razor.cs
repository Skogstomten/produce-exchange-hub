namespace ProduceExchangeHub.Pages;

public partial class Index : ComponentBase
{
    private List<CompanyListModel>? Companies { get; set; }

    [Inject]
    protected ICompanyService CompanyService { get; set; } = default!;

    protected override async Task OnInitializedAsync()
    {
        Companies = await CompanyService.GetCompaniesAsync(0, 10, SortOrder.Descending, "created_date");
    }
}
