"""Helpers for http stuff."""


def is_successfull(http_response_code: int) -> bool:
    """
    Checks if http response code is within success range.

    >>> is_successfull(103)
    False

    >>> is_successfull(200)
    True

    >>> is_successfull(226)
    True

    >>> is_successfull(300)
    False

    :param http_response_code:
    :return:
    """
    if 200 <= http_response_code < 300:
        return True
    return False
