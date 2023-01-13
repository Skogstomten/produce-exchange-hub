from django.http import HttpRequest, HttpResponseNotFound


def post_only(function):
    def wrapper(*args, **kwargs):
        request: HttpRequest = next(arg for arg in args if isinstance(arg, HttpRequest))
        if request.method != "POST":
            return HttpResponseNotFound()
        return function(*args, **kwargs)

    return wrapper
