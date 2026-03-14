from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from apps.core.constants.default_values import Role
from apps.core.utilities.authentication import CookieJWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken


def auth_required(login_url="/login/"):
    """
    Restrict access to logged-in users.
    Example:
        @auth_required(login_url="/custom_login/")
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(login_url)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return _adapt_decorator(decorator)


def anonymous_required(redirect_url="/"):
    """    
    Restrict access to non-logged-in users.
    If a logged-in user tries to access the view, redirect them.    
    Example:
        @anonymous_required(redirect_url="/dashboard/")
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_url)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return _adapt_decorator(decorator)


def role_required(*allowed_roles):
    """
    Restrict access based on user role(s).
    Example:
        @role_required(Role.ADMIN)
        @role_required(Role.DOCTOR, Role.ADMIN)
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user_role = getattr(request.user, "role", None)

            if user_role in [r.value for r in allowed_roles]:
                return view_func(request, *args, **kwargs)

            return HttpResponseForbidden("You do not have permission to access this page.")
        return _wrapped_view
    return _adapt_decorator(decorator)


def _adapt_decorator(decorator_func):
    """
    Make a decorator work for both FBV and CBV.
    """
    def wrapper(obj):
        if isinstance(obj, type):  # Class-based view
            obj.dispatch = method_decorator(decorator_func)(obj.dispatch)
            return obj
        return decorator_func(obj)  # Function-based view
    return wrapper


# Specific role-based decorators
# Examples:
    # @patient_required(login_url="/custom_login/")
    # @doctor_required(login_url="/custom_login/")
    # @admin_required(login_url="/custom_login/")    

def patient_required(view_or_func=None, *, login_url="/login/"):
    decorator = role_required(Role.PATIENT)
    if view_or_func:
        return auth_required(login_url=login_url)(decorator(view_or_func))
    return lambda view: auth_required(login_url=login_url)(decorator(view))


def doctor_required(view_or_func=None, *, login_url="/login/"):
    decorator = role_required(Role.DOCTOR)
    if view_or_func:
        return auth_required(login_url=login_url)(decorator(view_or_func))
    return lambda view: auth_required(login_url=login_url)(decorator(view))


def admin_required(view_or_func=None, *, login_url="admin/login/"):
    decorator = role_required(Role.ADMIN)
    if view_or_func:
        return auth_required(login_url=login_url)(decorator(view_or_func))
    return lambda view: auth_required(login_url=login_url)(decorator(view))



def get_user_from_jwt(request):
    """
    Tries to authenticate using JWT from cookie or header.
    Returns user object if valid, else None.
    """
    auth = CookieJWTAuthentication()
    try:
        result = auth.authenticate(request)
        if result is None:
            return None  # no token found
        user, token = result
        return user
    except (InvalidToken, TokenError):
        return None