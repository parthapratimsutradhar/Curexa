from apps.accounts.models import User
from apps.core.constants.default_values import Role
import secrets
from django.db import transaction
from apps.accounts.models.patientprofile_model import PatientProfile
from apps.doctors.models.doctorprofile_model import DoctorProfile
from django.shortcuts import get_object_or_404
from apps.core.utilities.email import send_email_template


def create_doctor_user(first_name, middle_name, last_name, email):
    """
    Create a user with doctor role.
    """
    user = User(
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        email=email,        
        role=Role.DOCTOR.value,
    )
    temp_password = secrets.token_urlsafe(12)
    user.set_password(temp_password)
    # ensure_user_profile(user)
    send_email_template(
        subject="Your Password for Doctor Account",
        recipient_email=email,
        template_name="emails/base_template.html",  # create this template
        context={
            "user_name": "Doctor",  # or doctor's actual name
            "message_title": "Your Temporary Password",
            "message_content": "Please use the password below to login and change it immediately.",
            "otp": temp_password,  # reuse otp field for password display
            "button_text": "Login Now",
            "button_url": "http://127.0.0.1:8000/doctor/login/"  # change to production URL later
        }
    )
    user.save()
    
    return user


@transaction.atomic
def ensure_user_profile(user):
    """
    Ensure a profile exists for the given user based on role.
    """
    if user.role == Role.PATIENT.value:
        profile, _ = PatientProfile.objects.get_or_create(
            patient=user
        )
        return profile

    if user.role == Role.DOCTOR.value:
        profile, _ = DoctorProfile.objects.get_or_create(
            doctor=user,
            experience_years=3
        )
        return profile

    raise ValueError(f"Unsupported user role: {user.role}")


def delete_doctor(user_id: int):
    user = get_object_or_404(User, id=user_id, role=Role.DOCTOR.value)

    user.is_active = False
    user.save(update_fields=["is_active"])

    DoctorProfile.objects.filter(doctor=user).delete()

    
def get_user_details(user):
    return get_object_or_404(User, id=user, is_active=True)