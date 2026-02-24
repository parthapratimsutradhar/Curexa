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




   
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q

def doctor_list_api(request):
    qs = doctor_services.doctor_queryset()

    search = request.GET.get("search", "").strip()
    status = request.GET.get("status", "")
    specialization = request.GET.get("specialization", "")

    if search:
        qs = qs.filter(
            Q(doctor__first_name__icontains=search) |
            Q(doctor__last_name__icontains=search) |
            Q(doctor__email__icontains=search)
        )

    if specialization:
        qs = qs.filter(specialization__name=specialization)

    # ✅ STATUS FILTER
    if status == "active":
        qs = qs.filter(is_available_today=True)
    elif status == "on_leave":
        qs = qs.filter(is_available_today=False)

    paginator = Paginator(qs, 5)
    page_obj = paginator.get_page(request.GET.get("page", 1))

    return JsonResponse({
        "results": doctor_services.doctor_list_data(page_obj),
        "page": page_obj.number,
        "pages": paginator.num_pages,
        "has_next": page_obj.has_next(),
        "has_prev": page_obj.has_previous(),
    })
