from apps.admin_panel import views
from django.urls import path

urlpatterns = [
    # Authentication
    path("admin/login/", views.AdminLoginView.as_view(), name="admin_login"),
    path("admin/logout/", views.AdminLogoutView.as_view(), name="admin_logout"),

    # Dashboard
    path("admin/", views.AdminDashboardView.as_view(), name="admin_dashboard"),
    path("admin/profile/", views.AdminProfileView.as_view(), name="admin_profile"),
    path("admin/profile/update", views.AdminProfileView.as_view(), name="admin_profile_update"),
    
    # Doctors
    path("admin/doctors/", views.DoctorListView.as_view(), name="doctor-list"),
    path("admin/doctors/add/", views.DoctorAddView.as_view(), name="doctor_add"),
    path("admin/doctors/<int:pk>/detail/", views.DoctorDetailView.as_view(), name="doctor_detail"),
    path("admin/doctors/<int:pk>/edit/", views.DoctorEditView.as_view(), name="doctor_edit"),
    path("admin/doctors/<int:pk>/delete/", views.DoctorDeleteView.as_view(), name="doctor_delete"),
    path("admin/doctors/schedules/", views.DoctorsSchedulesView.as_view(), name="doctors_schedules"),
    path("admin/doctor/<int:pk>/schedules/", views.DoctorSchedulesView.as_view(), name="doctor_schedules"),
    
    # Patients
    path("admin/patients/", views.PatientListView.as_view(), name="patient_list"),
    path("admin/patients/add/", views.PatientAddView.as_view(), name="patient_add"),
    path("admin/patients/<int:pk>/medical-records/", views.PatientMedicalRecordsView.as_view(), name="patient_medical_records"),
    
    # Appointments
    path("admin/appointments/", views.AppointmentListView.as_view(), name="appointment_list"),
    path("admin/appointments/appointment-history/", views.AppointmentHistoryView.as_view(), name="appointment_history"),
    path("admin/appointments/add/", views.AppointmentAddView.as_view(), name="appointment_add"),

    # Medicines
    path("admin/medicines/", views.MedicineListView.as_view(), name="medicine_list"),
    path("admin/medicines/add/", views.MedicineAddView.as_view(), name="medicine_add"),
    path("admin/medicines/<int:pk>/edit/", views.MedicineEditView.as_view(), name="medicine_edit"),
    
    # Categories
    path("admin/categories/", views.CategoryListView.as_view(), name="category_list"),
    
    # Inventory
    path("admin/inventory/", views.InventoryListView.as_view(), name="inventory_list"),
    
    # Reports
    path("admin/reports/sales", views.SalesReportsView.as_view(), name="sales_reports"),
    path("admin/reports/inventory", views.InventoryReportsView.as_view(), name="inventory_reports"),
    path("admin/reports/appoinment", views.AppointmentReportsView.as_view(), name="appoinment_reports"),
    
]
