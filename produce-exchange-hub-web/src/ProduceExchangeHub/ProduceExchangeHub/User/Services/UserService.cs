using ProduceExchangeHub.Shared.Localization.Services;
using ProduceExchangeHub.Shared.Providers;
using ProduceExchangeHub.Shared.Services;
using ProduceExchangeHub.User.Models;

namespace ProduceExchangeHub.User.Services;

public class UserService : ServiceBase, IUserService
{
    public UserService(
        HttpClient httpClient,
        ICultureService cultureService,
        ILogger<UserService> logger,
        IAccessTokenProvider accessTokenProvider
    )
        : base(httpClient, cultureService, logger, accessTokenProvider)
    {
    }

    public Task<RegisterUserResponseModel> RegisterUserAsync(RegisterModel model) =>
        PostAsync<RegisterModel, RegisterUserResponseModel>("users/register", model);
}