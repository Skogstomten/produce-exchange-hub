from django.http import HttpRequest, HttpResponseForbidden


class SelfDecorator:
    def __init__(self, user_id_param_name):
        self.user_id_param_name = user_id_param_name

    def __call__(self, function):
        def wrapper(*args, **kwargs):
            request = next(arg for arg in args if isinstance(arg, HttpRequest))
            user_id = kwargs.get(self.user_id_param_name)
            if request.user.id == user_id:
                return function(*args, **kwargs)
            return HttpResponseForbidden()
        return wrapper


def self(user_id_param_name="user_id"):
    if callable(user_id_param_name):
        return SelfDecorator("user_id")(user_id_param_name)
    return SelfDecorator(user_id_param_name)
