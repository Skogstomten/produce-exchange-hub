﻿using Microsoft.AspNetCore.Components;
using Microsoft.Extensions.Localization;
using Microsoft.JSInterop;
using ProduceExchangeHub.Security.Abstractions;
using ProduceExchangeHub.User.Models;

namespace ProduceExchangeHub.User.Pages;

public partial class Login
{
    [Inject]
    private IAuthenticationManager AuthenticationManager { get; set; } = null!;
    
    [Inject]
    private NavigationManager NavigationManager { get; set; } = null!;

    [Inject]
    private IStringLocalizer<Login> Loc { get; set; } = null!;
    
    [Inject]
    private IJSRuntime JS { get; set; } = null!;

    [Parameter, SupplyParameterFromQuery(Name = "returnUrl")]
    public string? ReturnUrl { get; set; }

    private LoginModel _loginModel = new();

    protected override async Task OnAfterRenderAsync(bool firstRender)
    {
        await JS.InvokeVoidAsync("setFocus", "username");
        await base.OnAfterRenderAsync(firstRender);
    }

    public async Task LoginEventHandler()
    {
        LoginResult result = await AuthenticationManager.LoginAsync(_loginModel.Username, _loginModel.Password);
        if (result == LoginResult.Success)
        {
            _loginModel = new LoginModel();
            NavigationManager.NavigateTo(string.IsNullOrWhiteSpace(ReturnUrl) ? "/" : ReturnUrl);
        }
    }
}