# apps/accounts/serializers/patient_resolve.py

from rest_framework import serializers
from apps.accounts.models import User, PatientProfile
from apps.core.constants.default_values import Role


class PatientResolveSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=55, required=False)
    last_name = serializers.CharField(max_length=55, required=False)
    phone_number = serializers.CharField(max_length=15, required=False)

    def create(self, validated_data):
        email = validated_data["email"]

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "first_name": validated_data.get("first_name", ""),
                "last_name": validated_data.get("last_name", ""),
                "role": Role.PATIENT.value
            }
        )

        # Ensure patient profile exists
        PatientProfile.objects.get_or_create(
            patient=user,
            defaults={
                "phone_number": validated_data.get("phone_number")
            }
        )

        return user, created
