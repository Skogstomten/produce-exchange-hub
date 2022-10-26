using ProduceExchangeHub.Company.Models;
using ProduceExchangeHub.Shared.Localization.Services;
using ProduceExchangeHub.Shared.Services;

namespace ProduceExchangeHub.Company.Services;

public class AddressService : ServiceBase, IAddressService
{
    public AddressService(HttpClient httpClient, ICultureService cultureService, ILogger<AddressService> logger)
        : base(httpClient, cultureService, logger)
    {
    }

    public Task<IEnumerable<AddressModel>> GetCompanyAddressesAsync(string companyID)
    {
        return GetAsync<IEnumerable<AddressModel>>($"companies/{companyID}/addresses/");
    }
}