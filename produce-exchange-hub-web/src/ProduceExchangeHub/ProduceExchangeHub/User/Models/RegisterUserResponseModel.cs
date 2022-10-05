using System.Text.Json.Serialization;

namespace ProduceExchangeHub.User.Models;

public class RegisterUserResponseModel
{
    [JsonPropertyName("email")]
    public string EMail { get; set; } = null!;

    [JsonPropertyName("firstname")]
    public string FirstName { get; set; } = null!;

    [JsonPropertyName("lastname")]
    public string LastName { get; set; } = null!;

    [JsonPropertyName("city")]
    public string? City { get; set; }

    [JsonPropertyName("country_iso")]
    public string Country { get; set; } = null!;

    [JsonPropertyName("timezone")]
    public string Timezone { get; set; } = null!;

    [JsonPropertyName("language_iso")]
    public string Language { get; set; } = null!;

    [JsonPropertyName("verified")]
    public bool Verified { get; set; }
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
  "created": "2022-10-05T19:42:16.342Z",
  "last_logged_in": "2022-10-05T19:42:16.342Z",
  "roles": [],
  "profile_picture_url": "string"
}
*/