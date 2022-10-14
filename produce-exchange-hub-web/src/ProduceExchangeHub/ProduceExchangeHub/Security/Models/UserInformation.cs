namespace ProduceExchangeHub.Security.Models;

public record UserInformation(
    string? Id,
    string? FirstName,
    string? LastName,
    string? EMail,
    bool Verified,
    IEnumerable<string> Roles
);