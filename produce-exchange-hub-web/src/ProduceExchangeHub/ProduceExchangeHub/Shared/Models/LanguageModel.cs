﻿using System.Text.Json.Serialization;

namespace ProduceExchangeHub.Shared.Models;

public class LanguageModel
{
    [JsonPropertyName("ISO_code")]
    public string ISOCode { get; set; } = string.Empty;

    [JsonPropertyName("name")]
    public string Name { get; set; } = string.Empty;
}