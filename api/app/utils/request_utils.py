from fastapi import Request

from .query.query_parameter import QueryParameter


def get_current_request_url_with_additions(
        request: Request,
        extra_path_parameters: tuple[str] = (),
        query_parameters: tuple[QueryParameter] = (),
) -> str:
    url = str(request.url)
    if not url.endswith('/'):
        url += '/'

    for path_parameter in extra_path_parameters:
        url += f"{path_parameter}/"

    if len(query_parameters) > 0:
        url += '?'
        for query_parameter in query_parameters:
            url += query_parameter.param_name
            for index, value in enumerate(query_parameter.values):
                if index == 0:
                    url += f"={value}"
                else:
                    url += f"{query_parameter.param_name}={value}"

    return url
