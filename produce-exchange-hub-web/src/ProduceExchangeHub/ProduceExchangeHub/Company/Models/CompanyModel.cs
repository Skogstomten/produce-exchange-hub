using System.Text.Json.Serialization;

namespace ProduceExchangeHub.Company.Models
{
    public class CompanyModel : CompanyListModel
    {
        [JsonPropertyName("contacts")]
        public ContactModel[] Contacts { get; set; } = Array.Empty<ContactModel>();
    }
}
