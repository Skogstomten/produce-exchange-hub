using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace ProduceExchangeHub.User.Models;

public class RegisterModel
{
    [JsonPropertyName("email")]
    [Required(AllowEmptyStrings = false)]
    [EmailAddress]
    public string? EMail { get; set; }

    [JsonPropertyName("firstname")]
    [Required]
    public string? FirstName { get; set; }

    [JsonPropertyName("lastname")]
    [Required]
    public string? LastName { get; set; }

    [JsonPropertyName("city")]
    public string? City { get; set; }

    [JsonPropertyName("country_iso")]
    [Required]
    public string? Country { get; set; }

    [JsonPropertyName("timezone")]
    [Required]
    public string? Timezone { get; set; }

    [JsonPropertyName("language_iso")]
    [Required]
    public string? Language { get; set; }

    [JsonPropertyName("verified")]
    public bool Verified => true;

    [JsonPropertyName("password")]
    [Required]
    public string? Password { get; set; }
}