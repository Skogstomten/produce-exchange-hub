using Microsoft.AspNetCore.Components;
using Microsoft.Extensions.Localization;
using ProduceExchangeHub.Company.Models;
using ProduceExchangeHub.Company.Services;

namespace ProduceExchangeHub.Company.Pages;

public partial class Company
{
    [Parameter]
    public string ID { get; set; } = string.Empty;

    [Inject]
    private ICompanyService CompanyService { get; set; } = null!;

    [Inject]
    private IAddressService AddressService { get; set; } = null!;

    [Inject]
    private IStringLocalizer<Company> Loc { get; set; } = null!;

    private CompanyModel CompanyModel { get; set; } = new();
    private AddressModel[] AddressModels { get; set; } = Array.Empty<AddressModel>();

    protected override async Task OnInitializedAsync()
    {
        Task<CompanyModel> getCompany = CompanyService.GetCompanyAsync(ID);
        Task<IEnumerable<AddressModel>> getAddress = AddressService.GetCompanyAddressesAsync(ID);
        await Task.WhenAll(getCompany, getAddress);
        CompanyModel = await getCompany;
        AddressModels = (await getAddress).ToArray();
    }
}