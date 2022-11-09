using System.Text.Json.Serialization;

namespace ProduceExchangeHub.Company.Models;

public class AddressModel
{
    [JsonPropertyName("addressee")]
    public string? Addressee { get; set; }

    [JsonPropertyName("co_address")]
    public string? COAddress { get; set; }

    [JsonPropertyName("street_address")]
    public string? StreetAddress { get; set; }

    [JsonPropertyName("city")]
    public string? City { get; set; }

    [JsonPropertyName("zip_code")]
    public string? ZipCode { get; set; }

    [JsonPropertyName("country_code")]
    public string? CountryCode { get; set; }
}

/*
[
  {
    "id": "string",
    "addressee": "string",
    "co_address": "string",
    "street_address": "string",
    "city": "string",
    "zip_code": "string",
    "country_code": "SE"
  }
]
*/