using ProduceExchangeHub.Admin.Models;
using ProduceExchangeHub.Shared.Localization.Services;
using ProduceExchangeHub.Shared.Models;
using ProduceExchangeHub.Shared.Providers;
using ProduceExchangeHub.Shared.Services;

namespace ProduceExchangeHub.Admin.Services;

public class AdminService : ServiceBase, IAdminService
{
    public AdminService(
        HttpClient httpClient,
        ICultureService cultureService,
        ILogger<AdminService> logger,
        IAccessTokenProvider accessTokenProvider
    )
        : base(httpClient, cultureService, logger, accessTokenProvider)
    {
    }

    public Task<ListResponseModel<UserModel>> GetUsersAsync() => GetAsync<ListResponseModel<UserModel>>("users/");
    public Task<UserModel> GetUserAsync(string id) => GetAsync<UserModel>($"users/{id}");
}