# apps/core/authentication.py
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken
from django.conf import settings

class CookieJWTAuthentication(JWTAuthentication):
    """
    JWT Authentication using cookies instead of Authorization headers.

    How it works:
    1. Reads 'access' token from cookie by default (configurable via cookie_name)
    2. Converts it to Bearer token internally so SimpleJWT validates it
    3. Returns (user, token) for DRF views

    Optional:
    - You can also add 'refresh' cookie logic for token rotation
    """

    access_cookie_name = "access_token"       # Name of cookie storing access token
    refresh_cookie_name = "refresh_token"     # Name of cookie storing refresh token

    def get_header(self, request):
        """
        Override get_header to read token from cookie instead of Authorization header
        """
        raw_token = request.COOKIES.get(self.access_cookie_name)
        if raw_token:
            # SimpleJWT expects "Authorization: Bearer <token>"
            return b"Bearer " + raw_token.encode()
        return None

    def authenticate(self, request):
        """
        Full authenticate method uses SimpleJWT internals
        """
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token

    # Optional helper to refresh token (for rotation)
    def refresh_token(self, request):
        refresh_token = request.COOKIES.get(self.refresh_cookie_name)
        if not refresh_token:
            raise AuthenticationFailed("Refresh token missing")
        try:
            token = api_settings.REFRESH_TOKEN_CLASS(refresh_token)
            new_access = token.access_token
            return str(new_access)
        except Exception as e:
            raise InvalidToken("Invalid refresh token") from e
