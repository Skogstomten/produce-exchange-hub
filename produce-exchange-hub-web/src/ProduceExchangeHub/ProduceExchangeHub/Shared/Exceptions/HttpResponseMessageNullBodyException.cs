using System.Text;

namespace ProduceExchangeHub.Shared.Exceptions;

public class HttpResponseMessageNullBodyException : Exception
{
    public HttpResponseMessageNullBodyException(string url, HttpResponseMessage response, string? responseBody)
        : base(CreateMessage(url, response, responseBody))
    {
    }

    private static string CreateMessage(string url, HttpResponseMessage response, string? responseBody)
    {
        StringBuilder message = new();
        message.AppendLine("Received null or non json body in http response where a json body was expected.")
               .AppendLine($"Url='{url}'")
               .AppendLine($"HttpStatus={(int) response.StatusCode}({response.StatusCode})")
               .AppendLine("Body: " + responseBody);
        return message.ToString();
    }
}