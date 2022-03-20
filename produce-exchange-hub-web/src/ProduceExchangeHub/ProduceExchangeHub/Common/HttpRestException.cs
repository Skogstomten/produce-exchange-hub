﻿using System.Net;

namespace ProduceExchangeHub.Common;

public class HttpRestException : Exception
{
    public HttpRestException(HttpStatusCode httpStatusCode, string body)
        : base($"Http rest error. StatusCode={(int)httpStatusCode}, body={body}")
    {
    }
}
