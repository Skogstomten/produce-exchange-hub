from django.http import HttpRequest, HttpResponseForbidden


def self(user_id_param_name: str = "user_id"):
    def decorator(function):
        def wrapper(*args, **kwargs):
            request: HttpRequest = next(arg for arg in args if isinstance(arg, HttpRequest))
            user_id = kwargs.get(user_id_param_name)
            if not request.user.id == user_id:
                return HttpResponseForbidden()
            return function(*args, **kwargs)

        return wrapper

    return decorator
