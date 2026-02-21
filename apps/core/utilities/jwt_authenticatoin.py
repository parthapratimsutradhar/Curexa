from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from apps.core.utilities.authentication import CookieJWTAuthentication

def jwt_cookie_required(view_func):
    """
    Decorator to protect views using JWT from cookie or Authorization header.
    Redirects to login if token is missing, invalid, or expired.
    """
    from functools import wraps

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        auth = CookieJWTAuthentication()
        try:
            result = auth.authenticate(request)
            if result is None:
                return redirect("login")  # no token found
            user, token = result
            request.user = user
        except (InvalidToken, TokenError):
            return redirect("login")  # invalid or expired token

        return view_func(request, *args, **kwargs)

    return wrapper


class JWTRequiredMixin:
    """
    Mixin for CBVs to enforce JWT authentication.    
    """
    @method_decorator(jwt_cookie_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)