namespace ProduceExchangeHub.Shared.Exceptions;

public class HttpResponseMessageNullBodyException : Exception
{
    public HttpResponseMessageNullBodyException(string url, HttpResponseMessage response)
        : base(
            "Received null body in http response where a body was expected. " +
            $"Url='{url}', " +
            $"HttpStatus={(int) response.StatusCode}({response.StatusCode})"
        )
    {
    }
}