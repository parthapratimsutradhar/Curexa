# apps/core/authentication.py

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # 1️⃣ Try Authorization header first (optional, helpful)
        header = self.get_header(request)
        if header is not None:
            raw_token = self.get_raw_token(header)
        else:
            # 2️⃣ Fallback to cookie
            raw_token = request.COOKIES.get("access_token")

        if raw_token is None:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
        except InvalidToken as e:
            raise AuthenticationFailed("Invalid or expired token") from e

        user = self.get_user(validated_token)
        return user, validated_token
