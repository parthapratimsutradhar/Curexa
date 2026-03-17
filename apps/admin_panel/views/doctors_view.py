from django.views import View
from django.shortcuts import render, redirect
from apps.doctors.services import doctor_services, department_services, specialization_services, qualification_services
from apps.docbook.services import appointment_services, availability_services
from apps.accounts.services import user_services
from apps.core.utilities.decorators import admin_required
from django.http import JsonResponse

@admin_required(login_url="/admin/login/")
class DoctorListView(View):
    def get(self, request):
        specializations= specialization_services.get_all_specializations()
        doctors = doctor_services.doctor_list_data(
            doctor_services.doctor_queryset()[:5]
        )
        total_doctors=doctor_services.total_doctors_count()
        active_doctors=availability_services.today_active_doctors_count()
        specialized_doctors=doctor_services.specialized_doctors_count()

        context = {
            "doctors": doctors,
            "specializations": specializations,
            "total_doctors": total_doctors,
            "specialized_doctors": specialized_doctors,
            "active_doctors": active_doctors,
            "inactive_doctors_today": total_doctors - active_doctors,
        }

        return render(request, "admin/doctors/doctors_list.html", context)

@admin_required(login_url="/admin/login/")
class DoctorAddView(View):
    def get(self, request):
        departments = department_services.get_all_departments()
        specializations = specialization_services.get_all_specializations()
        return render(request, "admin/doctors/doctor_add.html", {"departments": departments, "specializations": specializations})

    def post(self, request):
        firstName = request.POST.get("firstName")
        middleName = request.POST.get("middleName")
        lastName = request.POST.get("lastName")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        clinic_address = request.POST.get("clinic_address")
        city = request.POST.get("city")
        pin_code = request.POST.get("pin_code")

        license_number = request.POST.get("licenseNumber")
        license_expiry = request.POST.get("licenseExpiry")

        specialization_id = request.POST.get("specialization")

        degree = request.POST.get("degree")
        institution = request.POST.get("institution")
        completion_year = request.POST.get("completion_year")

        experience = request.POST.get("experience")
        consultation_fee = request.POST.get("consultation_fee")
        bio = request.POST.get("bio")
        dob = request.POST.get("dob")

        profile_picture = request.FILES.get("profile_photo")

        # Create doctor user
        dr_user = user_services.create_doctor_user(
            firstName, middleName, lastName, email
        )
        
        specialization = specialization_services.get_specialization_by_id(specialization_id)

        doctor = doctor_services.doctor_add(
            dr_user=dr_user,
            license_number=license_number,
            license_expiry_date=license_expiry,
            profile_picture=profile_picture,
            consultation_fee=consultation_fee,
            specialization=specialization,
            experience_years=experience,
            bio=bio,
            dob=dob,
            clinic_address=clinic_address,
            city=city,
            pin_code=pin_code,
            contact_number=phone
        )
        qualification_services.add_qualification(
            doctor, degree, institution, completion_year
        )
        

        return redirect("doctor-list")

@admin_required(login_url="/admin/login/")
class DoctorDetailView(View):
    def get(self, request, pk):

        # DoctorProfile
        doctor_profile = doctor_services.get_doctor_by_id(pk)

        # Doctor details (expects User)
        dr = doctor_services.get_doctor_details(doctor_profile)
        
        qualifications = qualification_services.get_doctor_qualifications(pk)

        today_appointments = appointment_services.get_doctor_today_appointments(pk)        
        today_appointments_count = appointment_services.todays_appointments_count_by_doctor(pk)
        # print(today_appointments_count)

        upcoming_appointments = (
            appointment_services.get_doctor_next_week_appointments(pk)
        )

        unique_patients = (
            appointment_services.doctor_unique_patients_count(pk)
        )

        total_appointments_month = (
            appointment_services.doctor_appointments_count_this_month(pk)
        )
        total_appointments = (
            appointment_services.doctor_total_appointments_count(pk)
        )
        total_completed_appointments=(
            appointment_services.doctor_total_completed_appointments_count(pk)
        )
        completion_rate = (
            appointment_services.doctor_completion_rate(pk)
        )

        context = {
            "doctor": dr,
            "qualifications": qualifications,
            "today_appointments": today_appointments,
            "upcoming_appointments": upcoming_appointments,
            "unique_patients": unique_patients,
            "total_appointments_month": total_appointments_month,
            "completion_rate": completion_rate,
            "total_appointments":total_appointments,
            "today_appointments_count":today_appointments_count,
            "total_completed_appointments":total_completed_appointments
        }
        
        return render(
            request,
            "admin/doctors/doctor_detail.html",
            context
        )


@admin_required(login_url="/admin/login/")    
class DoctorEditView(View):
    def get(self, request, pk):
        return render(request, "admin/doctors/doctor_edit.html")
    
@admin_required(login_url="/admin/login/")
class DoctorDeleteView(View):
    def post(self, request, pk):
        user_services.delete_doctor(pk)
        return JsonResponse({
            "success": True,
            "message": "Doctor deleted successfully"
        })