def assemble_url(*args, **kwargs) -> str:
    """
    *************
    Examples:

    >>> assemble_url("http://localhost:8000/", "/v1/{lang}/companies", "619676eb51b9ece53cbccb9b")
    'http://localhost:8000/v1/{lang}/companies/619676eb51b9ece53cbccb9b'

    >>> assemble_url("http://localhost:8000/", "/v1/{lang}/companies", "619676eb51b9ece53cbccb9b", lang="sv")
    'http://localhost:8000/v1/sv/companies/619676eb51b9ece53cbccb9b'

    :param args:
    :return:
    """
    url = "/".join(str(s).strip("/") for s in args)
    for key, value in kwargs.items():
        url = url.replace("{" + key + "}", str(value))
    return url
