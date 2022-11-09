using System.IdentityModel.Tokens.Jwt;

namespace ProduceExchangeHub.Shared.Utilities;

public class JwtHelper
{
    public static JwtSecurityToken DecodeJwtToken(string jwtEncodedToken)
    {
        JwtSecurityTokenHandler tokenHandler = new();
        JwtSecurityToken jwtSecurityToken = tokenHandler.ReadJwtToken(jwtEncodedToken);
        return jwtSecurityToken;
    }
}