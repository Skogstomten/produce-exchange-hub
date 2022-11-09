using ProduceExchangeHub.Admin.Models;
using ProduceExchangeHub.Shared.Models;

namespace ProduceExchangeHub.Admin.Services;

public interface IAdminService
{
    Task<ListResponseModel<UserModel>> GetUsersAsync();
    Task<UserModel> GetUserAsync(string id);
    Task DeleteUserAsync(string id);
}