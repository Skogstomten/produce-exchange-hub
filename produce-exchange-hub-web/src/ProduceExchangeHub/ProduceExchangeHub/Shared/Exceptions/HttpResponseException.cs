using System.Net;
using ProduceExchangeHub.Shared.Models;

namespace ProduceExchangeHub.Shared.Exceptions;

public class HttpResponseException : Exception
{
    public HttpResponseException(string url, ErrorModel error, HttpStatusCode statusCode)
        : base(
            "Error received from rest call. " +
            $"url={url}, " +
            $"HttpStatus={(int) statusCode}({statusCode}), " +
            $"Detail='{error.Detail}'"
        )
    {
    }
}