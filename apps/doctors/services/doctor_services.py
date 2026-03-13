from apps.doctors.models.doctorprofile_model import DoctorProfile
from apps.doctors.models.qualification_model import Qualification
from apps.docbook.services import appointment_services
from django.db.models import Exists, OuterRef, Prefetch
from apps.docbook.models.availability_model import Availability
from django.utils.timezone import localdate
from django.shortcuts import get_object_or_404
from apps.core.services import util_services
from django.utils.dateparse import parse_date
from apps.core.utilities.cloudinary_utils import cloudinary_upload_files


def get_doctor_by_id(pk):
    return get_object_or_404(DoctorProfile, id=pk)


def doctor_queryset(date=None, doctor_id=None):
    selected_date = parse_date(date) if date else localdate()

    qs = DoctorProfile.objects.select_related(
        "doctor",
        "specialization",
        "specialization__department",
    )

    if doctor_id:
        qs = qs.filter(id=doctor_id)

    return qs.prefetch_related(
        "fk_qualifications_doctor_profile_doctor_id",
        Prefetch(
            "fk_doctor_availabilities_doctor_id",
            queryset=Availability.objects.filter(
                date=selected_date,
                is_active=True,
                is_available=True,
                is_leave=False,
            ).select_related(
                "fk_availability_appointment_availability_id"
            ).only(
                "id",
                "start_time",
                "end_time",
                "is_available",
                "fk_availability_appointment_availability_id",
            ),
            to_attr="selected_date_slots",
        )
    ).annotate(
        is_available_today=Exists(
            Availability.objects.filter(
                doctor=OuterRef("pk"),
                date=selected_date,
                is_active=True,
                is_leave=False,
            )
        ),
        appointment_today=appointment_services.todays_appointments_count_by_doctor_ref(
            OuterRef("pk")
        ),
        active_appointment_today=appointment_services.active_appointments_count_by_doctor_ref(
            OuterRef("pk")
        ),
    )

def doctor_list_data(qs):
    result = []

    for obj in qs:
        qualification_data = [
            {
                "degree": q.degree,
                "institution": q.institution,
                "completion_year": q.completion_year.year if q.completion_year else None,
            }
            for q in obj.fk_qualifications_doctor_profile_doctor_id.all()
        ]

        slots = []
        for slot in getattr(obj, "selected_date_slots", []):
            # ✅ SAFE access for reverse relation
            appointment = getattr(
                slot,
                "fk_availability_appointment_availability_id",
                None
            )

            slots.append({
                "availability_id": slot.id,
                "start_time": slot.start_time,
                "end_time": slot.end_time,
                "is_available": slot.is_available and appointment is None
            })

        result.append({
            "id": obj.id,
            "name": obj.doctor.get_full_name(),
            "email": obj.doctor.email,
            "specialization": obj.specialization.name if obj.specialization else "",
            "department": (
                obj.specialization.department.name
                if obj.specialization and obj.specialization.department
                else None
            ),
            "education": qualification_data,
            "contact_number": obj.contact_number,
            "profile_picture": obj.profile_picture if obj.profile_picture else "",
            "experience_years": obj.experience_years,
            "clinic_address": obj.clinic_address,
            "consultation_fee": obj.consultation_fee,
            "age": util_services.age_from_dob(obj.dob),

            "is_available": obj.is_available_today,
            "appointment_count": obj.appointment_today or 0,
            "active_appointment_count": obj.active_appointment_today or 0,

            "available_slots": slots,
        })

    return result

def doctor_add(dr_user, license_number, license_expiry_date, profile_picture,
               consultation_fee, experience_years, bio, dob, clinic_address, specialization=None, city=None, pin_code=None, contact_number=None):
    images_path = cloudinary_upload_files(profile_picture, folder_name="doctors")
    if not isinstance(images_path, list):
        images_path = [images_path]
    return DoctorProfile.objects.create(
        doctor=dr_user,
        license_number=license_number,
        license_expiry=license_expiry_date,        
        consultation_fee=consultation_fee,     
        specialization=specialization,
        experience_years=experience_years,
        bio=bio,
        dob=dob,
        clinic_address=clinic_address,
        city=city,
        pin_code=pin_code,
        contact_number=contact_number,
        profile_picture=images_path
    )

    
def total_doctors_count():
    return DoctorProfile.objects.count()

def specialized_doctors_count():
    return DoctorProfile.objects.filter(specialization__isnull=False).count()

def get_all_doctors():
    return DoctorProfile.objects.values(
        'id',        
        'doctor__first_name',
        'doctor__middle_name',
        'doctor__last_name',
        'profile_picture',
        'specialization__name'
    )


def get_doctor_details(doctor):
    data = (
        DoctorProfile.objects
        .select_related(
            "doctor",
            "specialization",
            "specialization__department"
        )
        .filter(doctor=doctor.doctor.id)
        .values(
            "id",
            "doctor__public_id",
            "doctor__first_name",
            "doctor__middle_name",
            "doctor__last_name",
            "doctor__email",
            "contact_number",
            "profile_picture",
            "specialization__name",
            "specialization__department__name",
            "bio",
            "experience_years",
            "clinic_address",
            "license_number",
            "license_expiry",
            "consultation_fee",
            "dob",
        )
        .first()
    )

    if not data:
        return None

    return {
        "id": data["id"],
        "public_id": data["doctor__public_id"],
        "doctor_name": util_services.full_name(
            data["doctor__first_name"],
            data["doctor__middle_name"],
            data["doctor__last_name"]
        ),
        "email": data["doctor__email"],
        "contact_number": data["contact_number"],
        "profile_picture": data["profile_picture"],
        "specialization": data["specialization__name"],
        "department": data["specialization__department__name"],
        "bio": data["bio"],
        "experience_years": data["experience_years"],
        "clinic_address": data["clinic_address"],
        "license_number": data["license_number"],
        "license_expiry": data["license_expiry"],
        "consultation_fee": data["consultation_fee"],
        "dob": data["dob"],
        "age":util_services.age_from_dob(data["dob"]),
        "is_available_today": not appointment_services.is_doctor_on_leave(doctor, localdate())
    }


def doctor_list(limit=None):
    # Prefetch related data to reduce N+1 queries
    doctors = (
        DoctorProfile.objects
        .select_related(
            "doctor",
            "specialization",
            "specialization__department"
        )
        .all()
    )

    if limit is not None:
        doctors = doctors[:limit]

    doctor_data_list = []

    for d in doctors:
        data = {
            "id": d.id,
            "public_id": d.doctor.public_id,
            "doctor_name": util_services.full_name(
                d.doctor.first_name,
                d.doctor.middle_name,
                d.doctor.last_name
            ),
            "profile_picture": d.profile_picture,
            "specialization": d.specialization.name if d.specialization else None,
            "department": d.specialization.department.name if d.specialization and d.specialization.department else None,
            "experience_years": d.experience_years,
            "clinic_address": d.clinic_address,
            "consultation_fee": d.consultation_fee,
            "age": util_services.age_from_dob(d.dob),
            "is_available_today":appointment_services.is_doctor_available_today(d, localdate())
        }
        doctor_data_list.append(data)

    return doctor_data_list
