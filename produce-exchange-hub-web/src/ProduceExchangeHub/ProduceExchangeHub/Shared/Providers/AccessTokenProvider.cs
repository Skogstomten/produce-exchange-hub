using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using ProduceExchangeHub.Shared.Models;
using ProduceExchangeHub.Shared.Services;
using ProduceExchangeHub.Shared.Utilities;

namespace ProduceExchangeHub.Shared.Providers;

public class AccessTokenProvider : IAccessTokenProvider
{
    private readonly ILocalStorage _localStorage;

    public AccessTokenProvider(ILocalStorage localStorage)
    {
        _localStorage = localStorage;
    }

    public async Task<string?> GetAccessTokenAsync()
    {
        OAuthTokens? oAuthTokens = await _localStorage.GetAsync<OAuthTokens>(StorageKey.OAuthTokens);
        if (oAuthTokens != null)
        {
            JwtSecurityToken jwtToken = JwtHelper.DecodeJwtToken(oAuthTokens.AccessToken);
            Claim? expirationDate = jwtToken.Claims.FirstOrDefault(c => c.Type == "exp");
            if (expirationDate != null)
            {
                if (long.TryParse(expirationDate.Value, out long unixTime))
                {
                    DateTimeOffset timeOffset = DateTimeOffset.FromUnixTimeSeconds(unixTime);
                    DateTime now = DateTime.UtcNow;
                    if (now < timeOffset)
                    {
                        return oAuthTokens.AccessToken;
                    } else
                    {
                        await _localStorage.RemoveValuesAsync(StorageKey.OAuthTokens, StorageKey.UserInformation);
                    }
                }
            }
        }

        return null;
    }
}