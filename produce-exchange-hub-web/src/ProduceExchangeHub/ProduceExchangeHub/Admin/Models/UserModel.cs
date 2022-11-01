using System.Text.Json.Serialization;

namespace ProduceExchangeHub.Admin.Models;

public class UserModel
{
    [JsonPropertyName("id")]
    public string Id { get; set; } = null!;

    [JsonPropertyName("email")]
    public string Email { get; set; } = null!;

    [JsonPropertyName("firstname")]
    public string FirstName { get; set; } = null!;

    [JsonPropertyName("lastname")]
    public string LastName { get; set; } = null!;

    [JsonPropertyName("city")]
    public string City { get; set; } = null!;

    [JsonPropertyName("country_iso")]
    public string CountryISO { get; set; } = null!;

    [JsonPropertyName("timezone")]
    public string Timezone { get; set; } = null!;

    [JsonPropertyName("language_iso")]
    public string LanguageISO { get; set; } = null!;

    [JsonPropertyName("verified")]
    public bool Verified { get; set; }

    [JsonPropertyName("created")]
    public DateTime Created { get; set; }

    [JsonPropertyName("last_logged_in")]
    public DateTime? LastLoggedIn { get; set; }

    [JsonPropertyName("roles")]
    public UserRoleModel[] Roles { get; set; } = null!;

    [JsonPropertyName("profile_picture_url")]
    public string ProfilePictureUrl { get; set; } = null!;
}

/*
{
  "operations": [],
  "url": "",
  "email": "string",
  "firstname": "string",
  "lastname": "string",
  "city": "string",
  "country_iso": "SE",
  "timezone": "Europe/Stockholm",
  "language_iso": "SV",
  "verified": true,
  "id": "string",
  "created": "2022-11-01T07:34:36.164Z",
  "last_logged_in": "2022-11-01T07:34:36.165Z",
  "roles": [],
  "profile_picture_url": "string"
}
*/