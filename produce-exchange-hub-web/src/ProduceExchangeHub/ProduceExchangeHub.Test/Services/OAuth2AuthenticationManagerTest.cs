using System;
using System.IdentityModel.Tokens.Jwt;
using System.Threading.Tasks;
using NSubstitute;
using NSubstitute.ReturnsExtensions;
using NUnit.Framework;
using ProduceExchangeHub.Models;
using ProduceExchangeHub.Security;
using ProduceExchangeHub.Services;

namespace ProduceExchangeHub.Test.Services;

public class OAuth2AuthenticationManagerTest
{
    private IAuthenticationManager _target = null!;

    private readonly IAuthenticationService _authenticationService = Substitute.For<IAuthenticationService>();
    private readonly ILocalStorage _localStorage = Substitute.For<ILocalStorage>();

    [SetUp]
    public void Setup()
    {
        _target = new OAuth2AuthenticationManager(_authenticationService, _localStorage);
    }

    [Test]
    public async Task GetAuthenticatedUserAsyncReturnsFalseIfNoToken()
    {
        _localStorage.GetAsync<OAuthTokens>(default).ReturnsNullForAnyArgs();

        bool result = await _target.IsUserAuthenticatedAsync();

        Assert.IsFalse(result);
    }

    [Test]
    public async Task GetAuthenticatedUserAsyncReturnsFalseIfTokenExpired()
    {
        OAuthTokens tokens = GetOAuthTokens(DateTime.UtcNow.AddSeconds(-10));
        _localStorage.GetAsync<OAuthTokens>(StorageKey.OAuthTokens).Returns(tokens);

        bool result = await _target.IsUserAuthenticatedAsync();

        Assert.IsFalse(result);
    }
    
    [Test]
    public async Task GetAuthenticatedUserAsyncReturnsTrueIfValidTokenExists()
    {
        OAuthTokens tokens = GetOAuthTokens(DateTime.UtcNow.AddSeconds(10));
        _localStorage.GetAsync<OAuthTokens>(StorageKey.OAuthTokens).Returns(tokens);

        bool result = await _target.IsUserAuthenticatedAsync();

        Assert.IsTrue(result);
    }

    private static OAuthTokens GetOAuthTokens(DateTime expires)
    {
        JwtSecurityToken jwtSecurityToken = new(expires: expires);
        JwtSecurityTokenHandler handler = new();
        string accessTokenString = handler.WriteToken(jwtSecurityToken);
        OAuthTokens tokens = new() { AccessToken = accessTokenString };
        return tokens;
    }
}