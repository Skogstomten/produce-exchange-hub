namespace ProduceExchangeHub.Models;

public record UserInformation(
    string? Id,
    string? FirstName,
    string? LastName,
    string? EMail,
    bool Verified,
    IEnumerable<string> Roles
);