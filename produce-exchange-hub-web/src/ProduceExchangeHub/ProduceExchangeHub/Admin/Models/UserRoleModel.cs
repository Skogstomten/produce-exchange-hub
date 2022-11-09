using System.Text.Json.Serialization;

namespace ProduceExchangeHub.Admin.Models;

public class UserRoleModel
{
    [JsonPropertyName("id")]
    public string Id { get; set; } = null!;

    [JsonPropertyName("role_id")]
    public string RoleId { get; set; } = null!;

    [JsonPropertyName("role_name")]
    public string RoleName { get; set; } = null!;

    [JsonPropertyName("role_type")]
    public string RoleType { get; set; } = null!;

    [JsonPropertyName("reference")]
    public string? Reference { get; set; }
}

/*
id: str
role_id: str
role_name: str
role_type: RoleType
reference: str | None
*/