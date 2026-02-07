from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTCookieAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_auth = JWTAuthentication()

    def __call__(self, request):
        raw_token = request.COOKIES.get("access_token")

        if raw_token:
            try:
                validated_token = self.jwt_auth.get_validated_token(raw_token)
                request.user = self.jwt_auth.get_user(validated_token)
            except Exception:
                request.user = AnonymousUser()
        else:
            request.user = AnonymousUser()

        return self.get_response(request)
