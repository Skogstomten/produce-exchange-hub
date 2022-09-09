using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;

namespace ProduceExchangeHub.Common;

public class JwtHelper
{
    public static IEnumerable<Claim> DecodeJwtToken(string jwtEncodedToken)
    {
        JwtSecurityTokenHandler tokenHandler = new();
        JwtSecurityToken jwtSecurityToken = tokenHandler.ReadJwtToken(jwtEncodedToken);
        return jwtSecurityToken.Claims;
    }
}