using Microsoft.AspNetCore.Components;
using Microsoft.Extensions.Localization;

namespace ProduceExchangeHub.Admin.Pages;

public partial class Admin
{
    [Inject]
    private IStringLocalizer<Admin> Loc { get; set; } = null!;

    private Tab CurrentTab { get; set; } = Tab.UsersTab;

    private enum Tab
    {
        UsersTab
    }
}