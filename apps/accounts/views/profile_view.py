from django.views import View
from django.shortcuts import redirect, render
from apps.accounts.services import patient_services, user_services
# Api Configuration
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.serializers.patient_serializer import PatientResolveSerializer


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
        user=user_services.get_user_details(request.user.id)
        print("hiiiodnbnldnid:"+user)
        return render(request, "enduser/accounts/profile.html")
    
class EditProfileView(View):
    def get(self, request):
        return render(request, "enduser/accounts/edit_profile.html")