using System.ComponentModel.DataAnnotations;

namespace ProduceExchangeHub.Models;

public class LoginModel
{
    [Required]
    [EmailAddress]
    public string? Username { get; set; }

    [Required]
    public string? Password { get; set; }
}
