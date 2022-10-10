using ProduceExchangeHub.Shared.Localization.Services;
using ProduceExchangeHub.Shared.Services;
using ProduceExchangeHub.User.Models;

namespace ProduceExchangeHub.User.Services;

public class UserService : ServiceBase, IUserService
{
    public UserService(HttpClient httpClient, ICultureService cultureService)
        : base(httpClient, cultureService)
    {
    }

    public Task<RegisterUserResponseModel> RegisterUserAsync(RegisterModel model) =>
        PostAsync<RegisterModel, RegisterUserResponseModel>("users/register", model);
}