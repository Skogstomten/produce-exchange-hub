using ProduceExchangeHub.User.Models;

namespace ProduceExchangeHub.User.Services;

public interface IUserService
{
    Task<RegisterUserResponseModel> RegisterUserAsync(RegisterModel model);
}