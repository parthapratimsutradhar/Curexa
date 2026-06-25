from django.views import View
from django.shortcuts import redirect, render
from apps.accounts.services import patient_services, user_services
from apps.accounts.models.patientprofile_model import PatientProfile
from apps.accounts.models.users_model import User
from apps.core.constants.default_values import Role
# Api Configuration
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.serializers.patient_serializer import PatientResolveSerializer
from apps.core.services.util_services import full_name
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from apps.core.utilities.authentication import CookieJWTAuthentication



class GoogleLoginAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        credential = request.data.get("credential")

        if not credential:
            return Response(
                {"detail": "Missing credential"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verify token with Google
        try:
            info = id_token.verify_oauth2_token(
                credential,
                google_requests.Request(),
                settings.GOOGLE_CLIENT_ID,
                clock_skew_in_seconds=10,
            )
        except Exception:
            import traceback
            traceback.print_exc()
            return Response(
                {"detail": "Invalid Google token"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not info.get("email_verified"):
            return Response(
                {"detail": "Google email not verified"},
                status=status.HTTP_400_BAD_REQUEST
            )

        email = info["email"]
        full_name = info.get("name", "")
        avatar = info.get("picture")

        first_name = full_name.split(" ")[0]
        last_name = " ".join(full_name.split(" ")[1:]) if " " in full_name else ""

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "role": Role.PATIENT.value,
            }
        )

        # Always enforce patient role
        if user.role != Role.PATIENT.value:
            return Response(
                {"detail": "Unauthorized Access"},
                status=status.HTTP_400_BAD_REQUEST
            )

        profile, _ = PatientProfile.objects.get_or_create(patient=user)

        if created:
            user.set_unusable_password()
            user.save()

        if (first_name or last_name) and (not profile.patient.first_name and not profile.patient.last_name):
            profile.patient.first_name = first_name
            profile.patient.last_name = last_name
            profile.patient.save(update_fields=['first_name', 'last_name'])

        if avatar and not profile.profile_picture:
            profile.profile_picture = avatar
            profile.save()

        refresh = RefreshToken.for_user(user)

        response = Response(
            {
                "status": "success",
                "user": {
                    "email": user.email,
                    "name": user.get_full_name(),
                    "role": user.role,
                }
            },
            status=status.HTTP_200_OK
        )

        response.set_cookie(
            "access_token",
            str(refresh.access_token),
            httponly=True,
            secure=False,  # True in prod
            samesite="Lax",
            max_age=30 * 60,
        )

        response.set_cookie(
            "refresh_token",
            str(refresh),
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=7 * 24 * 60 * 60,
        )

        return response

class PatientResolveAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PatientResolveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user, created = serializer.save()

        refresh = RefreshToken.for_user(user)

        response = Response(
            {
                "status": "success",
                "is_new_user": created,
                "user": {
                    "public_id": user.public_id,
                    "name":full_name(user.first_name,user.middle_name,user.last_name),
                    "email": user.email,
                    "role": user.role
                }
            },
            status=status.HTTP_200_OK
        )

        response.set_cookie(
            "access_token",
            str(refresh.access_token),
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=30 * 60
        )

        response.set_cookie(
            "refresh_token",
            str(refresh),
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=7 * 24 * 60 * 60
        )

        return response

class ProfileView(View):
    def get(self, request):
        print(request)
        # user=user_services.get_user_details(request.user.id)
        # print("hiiiodnbnldnid:"+user)
        return render(request, "enduser/accounts/profile.html")
    
class EditProfileView(View):
    def get(self, request):
        return render(request, "enduser/accounts/edit_profile.html")
    
    
class MeAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]   # ✅ LIST

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
        })
    


@method_decorator(csrf_exempt, name="dispatch")
class LogoutAPIView(APIView):
    authentication_classes = []   # 🚫 no auth
    permission_classes = [AllowAny]

    def post(self, request):
        response = Response({"detail": "Logged out"})
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
