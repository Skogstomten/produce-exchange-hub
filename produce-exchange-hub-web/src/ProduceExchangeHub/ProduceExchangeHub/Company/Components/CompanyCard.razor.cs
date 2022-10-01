using Microsoft.AspNetCore.Components;
using ProduceExchangeHub.Company.Models;

namespace ProduceExchangeHub.Company.Components;

public partial class CompanyCard
{
    [Parameter]
    public CompanyListModel Company { get; set; } = new();
}
