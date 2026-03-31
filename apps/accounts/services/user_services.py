from apps.accounts.models import User
from apps.core.constants.default_values import Role
import secrets
from django.db import transaction
from apps.accounts.models.patientprofile_model import PatientProfile
from apps.doctors.models.doctorprofile_model import DoctorProfile
from django.shortcuts import get_object_or_404
from apps.core.utilities.email import send_email_template
from django.http import Http404

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


def delete_doctor(doctor_profile_id: int):
    updated = User.objects.filter(
        fk_doctor_doctor_profile_user_id__id=doctor_profile_id,
        role=Role.DOCTOR.value
    ).update(is_active=False)

    if not updated:
        raise Http404("Doctor not found")

    
def get_user_details(user):
    return get_object_or_404(User, id=user, is_active=True)


def toggle_doctor_status(doctor_profile_id, status: bool):
    doctor_profile = DoctorProfile.objects.select_related("doctor").get(
        id=doctor_profile_id,
        doctor__role=Role.DOCTOR.value
    )

    doctor_profile.doctor.is_active = status
    doctor_profile.doctor.save(update_fields=["is_active"])

    return doctor_profile