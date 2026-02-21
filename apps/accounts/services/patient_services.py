from apps.accounts.models.patientprofile_model import PatientProfile
from apps.core.services.util_services import full_name, age_from_dob
from django.shortcuts import get_object_or_404

def all_patients():
    qs = PatientProfile.objects.all().values(
        'patient__email',
        'gender',
        'dob',
        'patient__first_name',
        'patient__middle_name',
        'patient__last_name',
        'patient__last_login'
    )

    for q in qs:
        q['patient_name'] = full_name(
            q.pop('patient__first_name', ''),
            q.pop('patient__middle_name', ''),
            q.pop('patient__last_name', '')
        )

        q['last_login'] = q.pop('patient__last_login')

        dob = q.pop('dob', None)
        q['age'] = age_from_dob(dob) if dob else None

    return qs


def get_patient(user_id):
    return get_object_or_404(PatientProfile, patient_id=user_id)