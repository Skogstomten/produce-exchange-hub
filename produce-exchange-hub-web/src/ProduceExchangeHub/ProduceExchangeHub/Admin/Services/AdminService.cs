using ProduceExchangeHub.Admin.Models;
using ProduceExchangeHub.Shared.Localization.Services;
using ProduceExchangeHub.Shared.Models;
using ProduceExchangeHub.Shared.Services;

namespace ProduceExchangeHub.Admin.Services;

public class AdminService : ServiceBase, IAdminService
{
    public AdminService(HttpClient httpClient, ICultureService cultureService, ILogger logger)
        : base(httpClient, cultureService, logger)
    {
    }

    public Task<ListResponseModel<UserModel>> GetUsersAsync()
    {
        return GetAsync<ListResponseModel<UserModel>>("users/");
    }
}