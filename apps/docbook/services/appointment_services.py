from apps.docbook.models.appointment_model import Appointment
from apps.core.constants.default_values import AppointmentStatus, AppointmentType, Gender
from django.utils import timezone
from itertools import groupby
from operator import itemgetter
from apps.core.services.util_services import *
from apps.docbook.services.availability_services import *
from django.db.models import OuterRef, Subquery, Count, IntegerField, Q
from django.db.models.functions import Coalesce
from django.utils.timezone import localdate

def active_appointments_count(doctor):
    return Appointment.objects.filter(
                doctor=doctor,
                appointment_status=AppointmentStatus.SCHEDULED.value,
                availability__is_available=True,
                availability__date=timezone.now().date(),
            ).count()

def todays_appointments_count_by_doctor(doctor):
    return Appointment.objects.filter(
        doctor=doctor,
        availability__is_available=True,
        availability__date=timezone.localdate(),
        is_active=True
    ).exclude(
        appointment_status=AppointmentStatus.CANCELLED.value
    ).count()
    
def todays_appointments_count_for_all_doctors():
    return Appointment.objects.filter(
        availability__is_available=True,
        availability__is_active=True,
        availability__date=timezone.now().date(),
        is_active=True
    ).exclude(
        appointment_status=AppointmentStatus.CANCELLED.value
    ).count()

def todays_emergency_appointments_count():
    return Appointment.objects.filter(
        appointment_type=AppointmentType.EMERGENCY.value,
        is_active=True,
        availability__date=timezone.now().date()
    ).count()

def get_doctor_grouped_appointments(
    date=None,
    start_date=None,
    end_date=None,
    doctor_id=None,
    status=None,
    sort_by="start_time",
    order="asc",
):
    qs = Appointment.objects.filter(is_active=True)

    # ----------------------------
    # DB LEVEL FILTERS
    # ----------------------------
    if doctor_id:
        qs = qs.filter(doctor_id=doctor_id)

    if status:
        qs = qs.filter(appointment_status=status)

    if date:
        qs = qs.filter(
            availability__date=date,
            availability__is_active=True
        )
    elif start_date and end_date:
        qs = qs.filter(
            availability__is_active=True,
            availability__date__range=(start_date, end_date)
        )

    qs = qs.values(
        # Doctor
        'doctor__id',
        'doctor__doctor__first_name',
        'doctor__doctor__middle_name',
        'doctor__doctor__last_name',
        'doctor__profile_picture',
        'doctor__specialization__department__name',

        # Patient
        'patient__id',
        'patient__patient__first_name',
        'patient__patient__middle_name',
        'patient__patient__last_name',
        'patient__dob',
        'patient__gender',
        'patient__patient__email',
        'patient__phone_number',
        'patient__chronic_conditions',
        'patient__allergies',

        # Appointment
        'appointment_type',
        'appointment_status',
        'notes',

        # Availability
        'availability__date',
        'availability__start_time',
        'availability__end_time',
    )

    appointments = list(qs)

    # ----------------------------
    # DATA TRANSFORMATION
    # ----------------------------
    for a in appointments:
        a['doctor_id'] = a.pop('doctor__id')
        a['doctor_name'] = full_name(
            a.pop('doctor__doctor__first_name', ''),
            a.pop('doctor__doctor__middle_name', ''),
            a.pop('doctor__doctor__last_name', '')
        )
        a['doctor_profile_picture'] = a.pop('doctor__profile_picture')
        a['doctor_department'] = a.pop('doctor__specialization__department__name')

        a['patient_id'] = a.pop('patient__id')
        a['patient_name'] = full_name(
            a.pop('patient__patient__first_name', ''),
            a.pop('patient__patient__middle_name', ''),
            a.pop('patient__patient__last_name', '')
        )
        a['patient_email'] = a.pop('patient__patient__email')
        a['patient_age'] = age_from_dob(a.pop('patient__dob'))
        a['patient_gender'] = enum_name(Gender, a.pop('patient__gender'))
        a['patient_mobile'] = a.pop('patient__phone_number')
        a['patient_allergies'] = a.pop('patient__allergies')
        a['chronic'] = a.pop('patient__chronic_conditions')

        a['appt_type'] = enum_name(AppointmentType, a.pop('appointment_type'))
        a['appt_status'] = enum_name(AppointmentStatus, a.pop('appointment_status'))
        a['appt_notes'] = a.pop('notes')

        a['date'] = a.pop('availability__date')
        a['start_time'] = a.pop('availability__start_time')
        a['end_time'] = a.pop('availability__end_time')

    # ----------------------------
    # SORTING (Python level)
    # ----------------------------
    reverse = order == "desc"
    appointments.sort(key=itemgetter(sort_by), reverse=reverse)

    # ----------------------------
    # GROUP BY DOCTOR
    # ----------------------------
    appointments.sort(key=itemgetter('doctor_id'))
    grouped = {}

    for doctor_id, appts in groupby(appointments, key=itemgetter('doctor_id')):
        appts = list(appts)
        grouped[doctor_id] = {
            "doctor_name": appts[0]['doctor_name'],
            "appointments": appts
        }

    return grouped


def get_all_appointment_types_status():
    types = [
        {'name': t.name, 'value': t.value}
        for t in AppointmentType
    ]
    statuses = [
        {'name': s.name, 'value': s.value}
        for s in AppointmentStatus
    ]
    return {
        'types': types,
        'statuses': statuses
    }


def todays_appointments_count_by_doctor_ref(doctor_ref):
    return Subquery(
        Appointment.objects.filter(
            doctor=doctor_ref,
            availability__date=localdate()
        )
        .values("doctor")
        .annotate(c=Count("id"))
        .values("c"),
        output_field=IntegerField()
    )


def active_appointments_count_by_doctor_ref(doctor_ref):
    return Subquery(
        Appointment.objects.filter(
            doctor=doctor_ref,
            availability__date=localdate(),
            appointment_status=AppointmentStatus.SCHEDULED.value
        )
        .values("doctor")
        .annotate(c=Count("id"))
        .values("c"),
        output_field=IntegerField()
    )


def get_doctor_today_appointments(doctor_id):
    qs = Appointment.objects.filter(doctor_id=doctor_id, is_active=True, availability__date=localdate())

    qs = qs.values(
        # Patient
        'patient__id',
        'patient__patient__first_name',
        'patient__patient__middle_name',
        'patient__patient__last_name',
        'patient__dob',
        'patient__gender',
        'patient__patient__email',
        'patient__phone_number',
        'patient__chronic_conditions',
        'patient__allergies',

        # Appointment
        'appointment_type',
        'appointment_status',
        'notes',

        # Availability
        'availability__date',
        'availability__start_time',
        'availability__end_time',
    )

    appointments = list(qs)

    # ----------------------------
    # DATA TRANSFORMATION
    # ----------------------------
    for a in appointments:
        a['patient_id'] = a.pop('patient__id')
        a['patient_name'] = full_name(
            a.pop('patient__patient__first_name', ''),
            a.pop('patient__patient__middle_name', ''),
            a.pop('patient__patient__last_name', '')
        )
        a['patient_email'] = a.pop('patient__patient__email')
        a['patient_age'] = age_from_dob(a.pop('patient__dob'))
        a['patient_gender'] = enum_name(Gender, a.pop('patient__gender'))
        a['patient_mobile'] = a.pop('patient__phone_number')
        a['patient_allergies'] = a.pop('patient__allergies')
        a['chronic'] = a.pop('patient__chronic_conditions')

        a['appt_type'] = enum_name(AppointmentType, a.pop('appointment_type'))
        a['appt_status'] = enum_name(AppointmentStatus, a.pop('appointment_status'))
        a['appt_notes'] = a.pop('notes')

        a['date'] = a.pop('availability__date')
        a['start_time'] = a.pop('availability__start_time')
        a['end_time'] = a.pop('availability__end_time')
        
    return appointments


def get_doctor_next_week_appointments(doctor=None):
    start_date, end_date = get_current_week_range()
    qs = Appointment.objects.filter(doctor=doctor, is_active=True, availability__is_active=True,
            availability__date__range=(start_date, end_date) )
    qs = qs.values(
        # Doctor
        'doctor__profile_picture',
        'doctor__specialization__department__name',
        
        # Patient
        'patient__id',
        'patient__patient__first_name',
        'patient__patient__middle_name',
        'patient__patient__last_name',
        'patient__dob',
        'patient__gender',
        'patient__patient__email',
        'patient__phone_number',
        'patient__chronic_conditions',
        'patient__allergies',

        # Appointment
        'appointment_type',
        'appointment_status',
        'notes',

        # Availability
        'availability__date',
        'availability__start_time',
        'availability__end_time',
    )

    appointments = list(qs)

    for a in appointments:
        a['doctor_profile_picture'] = a.pop('doctor__profile_picture')
        a['doctor_department'] = a.pop('doctor__specialization__department__name')

        a['patient_id'] = a.pop('patient__id')
        a['patient_name'] = full_name(
            a.pop('patient__patient__first_name', ''),
            a.pop('patient__patient__middle_name', ''),
            a.pop('patient__patient__last_name', '')
        )
        a['patient_email'] = a.pop('patient__patient__email')
        a['patient_age'] = age_from_dob(a.pop('patient__dob'))
        a['patient_gender'] = enum_name(Gender, a.pop('patient__gender'))
        a['patient_mobile'] = a.pop('patient__phone_number')
        a['patient_allergies'] = a.pop('patient__allergies')
        a['chronic'] = a.pop('patient__chronic_conditions')

        a['appt_type'] = enum_name(AppointmentType, a.pop('appointment_type'))
        a['appt_status'] = enum_name(AppointmentStatus, a.pop('appointment_status'))
        a['appt_notes'] = a.pop('notes')

        a['date'] = a.pop('availability__date')
        a['start_time'] = a.pop('availability__start_time')
        a['end_time'] = a.pop('availability__end_time')

    return appointments

def doctor_unique_patients_count(doctor_id):
    qs = Appointment.objects.filter(
        doctor_id=doctor_id,
        is_active=True
    )
    return qs.values_list('patient_id', flat=True).distinct().count()


def doctor_appointments_count_this_month(doctor_id):
    return Appointment.objects.filter(
        doctor_id=doctor_id,
        is_active=True,
        availability__date__range=get_current_month_range()
    ).count()


def doctor_completion_rate(doctor_id):
    data = Appointment.objects.filter(
        doctor_id=doctor_id,
        is_active=True
    ).aggregate(
        total=Count(
            'id',
            filter=~Q(appointment_status=AppointmentStatus.SCHEDULED.value)
        ),
        completed=Count(
            'id',
            filter=Q(appointment_status=AppointmentStatus.COMPLETED.value)
        )
    )

    if not data['total']:
        return 0

    return round((data['completed'] / data['total']) * 100, 2)

def doctor_total_appointments_count(doctor_id):
        return Appointment.objects.filter(
        doctor_id=doctor_id,
    ).count()
        
def doctor_total_completed_appointments_count(doctor_id):
        return Appointment.objects.filter(
        doctor_id=doctor_id,
        appointment_status = AppointmentStatus.COMPLETED.value
    ).count()