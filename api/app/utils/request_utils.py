from fastapi import Request

from .query.query_parameter import QueryParameter


def get_current_request_url_with_additions(
    request: Request,
    extra_path_parameters: tuple[str] = (),
    query_parameters: tuple[QueryParameter] = (),
    include_query: bool = True,
) -> str:
    url = get_url(request)
    if not url.endswith("/"):
        url += "/"

    if include_query:
        url += get_query_string(request)

    for path_parameter in extra_path_parameters:
        url += f"{path_parameter}/"

    if len(query_parameters) > 0:
        url += "?"
        for query_parameter in query_parameters:
            url += query_parameter.param_name
            for index, value in enumerate(query_parameter.values):
                if index == 0:
                    url += f"={value}"
                else:
                    url += f"{query_parameter.param_name}={value}"

    return url


def get_url(request: Request) -> str:
    scheme = request.url.scheme
    host = request.url.hostname
    port = request.url.port
    path = request.url.path

    url = f"{scheme}://{host}"
    if port != 80:
        url += f":{str(port)}"
    url += path
    return url


def get_query_string(request: Request) -> str:
    query_string = ""
    for key in request.query_params:
        if query_string == "":
            query_string += "?"
        value = request.query_params[key]
        if query_string != "?":
            query_string += "&"
        query_string += str(key)
        if value:
            if value.strip() != "":
                query_string += f"={str(value)}"
    return query_string
