from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

class CookieJWTAuthentication(JWTAuthentication):
    
    """
    Custom JWT authentication class that extends DRF's JWTAuthentication.

    This class first attempts to authenticate the user using the standard
    Authorization header (Bearer <token>). If the header is missing, it falls
    back to checking for a JWT stored in a cookie named 'access_token'.

    This approach allows seamless authentication for browser-based clients
    that store tokens in cookies, while still supporting API clients that
    use Authorization headers.

    Returns:
        Tuple[user, validated_token] on successful authentication,
        or None if no token is found.
    
    Raises:
        AuthenticationFailed: if the token is invalid or expired.
    """

    def authenticate(self, request):
        # 1️⃣ Try Authorization header first
        header = self.get_header(request)
        raw_token = None

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