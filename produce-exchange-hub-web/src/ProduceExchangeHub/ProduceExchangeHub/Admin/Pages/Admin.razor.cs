using Microsoft.AspNetCore.Components;
using Microsoft.Extensions.Localization;
using Microsoft.JSInterop;

namespace ProduceExchangeHub.Admin.Pages;

public partial class Admin
{
    [Inject]
    private IStringLocalizer<Admin> Loc { get; set; } = null!;

    [Inject]
    private IJSRuntime JS { get; set; } = null!;

    private Tab CurrentTab { get; set; } = Tab.UsersTab;
    private ElementReference UsersTabRef { get; set; }
    private ElementReference DummyTabRef { get; set; }
    private ElementReference[] TabRefs { get; set; } = Array.Empty<ElementReference>();

    protected override async Task OnAfterRenderAsync(bool firstRender)
    {
        TabRefs = new[] {UsersTabRef, DummyTabRef};

        if (firstRender)
            await SetActiveTab(UsersTabRef, Tab.UsersTab);

        await base.OnAfterRenderAsync(firstRender);
    }

    private async Task SetActiveTab(ElementReference tabRef, Tab currentTab)
    {
        foreach (ElementReference elementRef in TabRefs)
            await JS.InvokeVoidAsync("removeClass", elementRef, "active");

        await JS.InvokeVoidAsync("addClass", tabRef, "active");
        CurrentTab = currentTab;
    }
    
    private enum Tab
    {
        UsersTab,
        DummyTab
    }
}