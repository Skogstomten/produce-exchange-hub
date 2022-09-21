using System.ComponentModel.DataAnnotations;

namespace ProduceExchangeHub.Models;

public class LoginModel
{
    [Required(AllowEmptyStrings = false)]
    [EmailAddress]
    public string Username { get; set; } = "";

    [Required(AllowEmptyStrings = false)]
    public string Password { get; set; } = "";
}
