using ProduceExchangeHub.Company.Models;

namespace ProduceExchangeHub.Company.Services;

public interface IAddressService
{
    Task<IEnumerable<AddressModel>> GetCompanyAddressesAsync(string companyID);
}