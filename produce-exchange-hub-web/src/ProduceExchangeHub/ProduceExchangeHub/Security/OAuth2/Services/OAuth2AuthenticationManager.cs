using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using ProduceExchangeHub.Security.Abstractions;
using ProduceExchangeHub.Security.Models;
using ProduceExchangeHub.Security.OAuth2.Tokens;
using ProduceExchangeHub.Security.Services;
using ProduceExchangeHub.Security.Utilities;
using ProduceExchangeHub.Shared.Models;
using ProduceExchangeHub.Shared.Services;
using ProduceExchangeHub.User.Models;

namespace ProduceExchangeHub.Security.OAuth2.Services;

public class OAuth2AuthenticationManager : IAuthenticationManager
{
    private readonly IAuthenticationService _authenticationService;
    private readonly ILocalStorage _localStorage;

    private readonly List<Func<AuthenticationEvent, Task>> _subscribers = new();

    private OAuthTokens? _oAuthTokens;
    private JwtSecurityToken? _jwtSecurityToken;

    public OAuth2AuthenticationManager(IAuthenticationService authenticationService, ILocalStorage localStorage)
    {
        _authenticationService = authenticationService;
        _localStorage = localStorage;
    }

    public async ValueTask<LoginResult> LoginAsync(string username, string password)
    {
        _oAuthTokens = await _authenticationService.AuthenticateAsync(username, password);

        _jwtSecurityToken = JwtHelper.DecodeJwtToken(_oAuthTokens.AccessToken);
        string? email = null, firstName = null, lastName = null, id = null;
        bool verified = false;
        List<string> roles = new();
        foreach (Claim claim in _jwtSecurityToken.Claims)
            switch (claim.Type)
            {
                case "email":
                    email = claim.Value;
                    break;
                case "given_name":
                    firstName = claim.Value;
                    break;
                case "family_name":
                    lastName = claim.Value;
                    break;
                case "id":
                    id = claim.Value;
                    break;
                case "verified":
                    verified = bool.Parse(claim.Value);
                    break;
                case "roles":
                    roles.Add(claim.Value);
                    break;
            }

        UserInformation userInformation = new(id, firstName, lastName, email, verified, roles);

        await _localStorage.SaveAsync(StorageKey.OAuthTokens, _oAuthTokens);
        await _localStorage.SaveAsync(StorageKey.UserInformation, userInformation);

        LoginResult result = LoginResult.Success;
        await NotifySubscribers(result);

        return result;
    }

    public async ValueTask LogoutAsync()
    {
        await _localStorage.RemoveValuesAsync(StorageKey.OAuthTokens, StorageKey.UserInformation);
    }

    public void Subscribe(Func<AuthenticationEvent, Task> callback) => _subscribers.Add(callback);

    public ValueTask<UserInformation?> GetAuthenticatedUserAsync() =>
        _localStorage.GetAsync<UserInformation>(StorageKey.UserInformation);

    public async ValueTask<bool> IsUserAuthenticatedAsync()
    {
        if (await GetJwtTokenAsync() == null)
            return false;
        return true;
    }

    private async ValueTask NotifySubscribers(LoginResult loginResult)
    {
        AuthenticationEvent e = new(loginResult);
        foreach (Func<AuthenticationEvent, Task> callback in _subscribers)
            await callback(e);
    }

    private async Task<JwtSecurityToken?> GetJwtTokenAsync()
    {
        if (_jwtSecurityToken == null)
        {
            _oAuthTokens ??= await _localStorage.GetAsync<OAuthTokens>(StorageKey.OAuthTokens);
            if (_oAuthTokens == null)
                return null;

            _jwtSecurityToken = JwtHelper.DecodeJwtToken(_oAuthTokens.AccessToken);
        }

        if (_jwtSecurityToken.ValidFrom < DateTime.UtcNow && _jwtSecurityToken.ValidTo > DateTime.UtcNow)
            return _jwtSecurityToken;
        _jwtSecurityToken = null;
        _oAuthTokens = null;
        await _localStorage.RemoveValuesAsync(StorageKey.OAuthTokens, StorageKey.UserInformation);
        return null;
    }
}