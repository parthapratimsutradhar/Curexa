from django.views import View
from django.shortcuts import redirect, render
from apps.doctors.services import doctor_services
class DoctorListView(View):
    def get(self, request):
        doctors = doctor_services.doctor_list()
        return render(request, "enduser/doctors/doctor_list.html", {"doctors":doctors})

class DoctorProfileView(View):
    def get(self, request, pk):
        return render(request, "enduser/doctors/doctor_profile.html")


class DoctorLoginView(View):
    def get(self, request):
        return render(request, "enduser(doctors)/doctor_login.html")


class DoctorPortalProfileView(View):
    def get(self, request):
        return render(request, "enduser(doctors)/doctor_profile.html")


class DoctorAppointmentManagementView(View):
    def get(self, request):
        return render(request, "enduser(doctors)/appointment_management.html")


class DoctorAvailabilityManagementView(View):
    def get(self, request):
        return render(request, "enduser(doctors)/availability_management.html")


class DoctorEarningView(View):
    def get(self, request):
        return render(request, "enduser(doctors)/doctor_earning.html")


class DoctorPrescriptionView(View):
    def get(self, request):
        return render(request, "enduser(doctors)/prescription.html")



   
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from django.utils.timezone import localdate

def doctor_list_api(request):
    date = request.GET.get("date")
    doctor_id = request.GET.get("doctor_id")

    qs = doctor_services.doctor_queryset(
        date=date,
        doctor_id=doctor_id
    )

    search = request.GET.get("search", "").strip()
    specialization = request.GET.get("specialization", "")

    if search:
        qs = qs.filter(
            Q(doctor__first_name__icontains=search) |
            Q(doctor__last_name__icontains=search) |
            Q(doctor__email__icontains=search)
        )

    if specialization:
        qs = qs.filter(specialization__name=specialization)

    paginator = Paginator(qs, 5)
    page_obj = paginator.get_page(request.GET.get("page", 1))

    return JsonResponse({
        "date": date or str(localdate()),
        "results": doctor_services.doctor_list_data(page_obj),
        "page": page_obj.number,
        "pages": paginator.num_pages,
        "has_next": page_obj.has_next(),
        "has_prev": page_obj.has_previous(),
    })
