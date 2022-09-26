﻿using Microsoft.AspNetCore.Components;
using ProduceExchangeHub.Models;

namespace ProduceExchangeHub.Components;

public partial class CompanyCard
{
    [Parameter]
    public CompanyListModel Company { get; set; } = new();
}
