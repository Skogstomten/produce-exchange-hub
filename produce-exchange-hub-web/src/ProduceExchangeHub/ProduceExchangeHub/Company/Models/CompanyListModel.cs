﻿using System.Text.Json.Serialization;

namespace ProduceExchangeHub.Company.Models;

public class CompanyListModel
{
    [JsonPropertyName("id")]
    public string Id { get; init; } = null!;

    [JsonPropertyName("name")]
    public string Name { get; set; } = null!;

    [JsonPropertyName("status")]
    public string Status { get; init; } = null!;

    [JsonPropertyName("created_date")]
    public DateTime CreatedDate { get; init; }

    [JsonPropertyName("company_types")]
    public string[] CompanyTypes { get; init; } = null!;

    [JsonPropertyName("content_languages_iso")]
    public string[] ContentLanguagesISO { get; init; } = null!;

    [JsonPropertyName("activation_date")]
    public DateTime? ActivationDate { get; init; }

    [JsonPropertyName("description")]
    public string? Description { get; init; }

    [JsonPropertyName("external_website_url")]
    public string? ExternalWebsiteUrl { get; init; }

    [JsonPropertyName("profile_picture_url")]
    public string? ProfilePictureUrl { get; init; }
}
