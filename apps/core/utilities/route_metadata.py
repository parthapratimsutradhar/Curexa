"""Human-readable metadata for Curexa URL routes."""

ROUTE_METADATA = {
    "home": {
        "description": "Main landing page with healthcare services overview and quick actions.",
        "methods": ["GET"],
        "auth": "public",
    },
    "login": {
        "description": "Patient login page with OTP and Google sign-in.",
        "methods": ["GET"],
        "auth": "public",
    },
    "logout": {
        "description": "Logs out the current session and redirects to home.",
        "methods": ["GET"],
        "auth": "authenticated",
    },
    "send_otp": {
        "description": "Sends a one-time password to the user's contact for authentication.",
        "methods": ["POST"],
        "auth": "public",
    },
    "verify_otp": {
        "description": "Verifies the OTP code submitted during login or signup.",
        "methods": ["POST"],
        "auth": "public",
    },
    "patient_profile": {
        "description": "Patient health dashboard and profile overview.",
        "methods": ["GET"],
        "auth": "authenticated",
    },
    "profile_edit": {
        "description": "Edit patient profile details and personal information.",
        "methods": ["GET"],
        "auth": "authenticated",
    },
    "emergency_care": {
        "description": "Emergency and urgent care information and resources.",
        "methods": ["GET"],
        "auth": "public",
    },
    "about": {
        "description": "About Curexa platform, mission, and team information.",
        "methods": ["GET"],
        "auth": "public",
    },
    "chat_page": {
        "description": "AI health assistant chatbot interface for symptom guidance.",
        "methods": ["GET"],
        "auth": "public",
    },
    "chat_api": {
        "description": "Backend endpoint powering the health chatbot responses.",
        "methods": ["POST"],
        "auth": "public",
    },
    "route_documentation": {
        "description": "Interactive documentation for all Curexa web and API routes.",
        "methods": ["GET"],
        "auth": "public",
    },
    "admin_login": {
        "description": "Administrator login portal for the admin dashboard.",
        "methods": ["GET", "POST"],
        "auth": "public",
    },
    "admin_logout": {
        "description": "Logs out the current admin session.",
        "methods": ["GET"],
        "auth": "admin",
    },
    "admin_dashboard": {
        "description": "Admin dashboard with platform metrics and quick actions.",
        "methods": ["GET"],
        "auth": "admin",
    },
    "admin_profile": {
        "description": "View and manage the logged-in admin's profile.",
        "methods": ["GET"],
        "auth": "admin",
    },
    "admin_profile_update": {
        "description": "Update admin profile information.",
        "methods": ["POST", "PUT", "PATCH"],
        "auth": "admin",
    },
    "doctor-list": {
        "description": "List all registered doctors in the admin panel.",
        "methods": ["GET"],
        "auth": "admin",
    },
    "doctor_add": {
        "description": "Add a new doctor to the platform.",
        "methods": ["GET", "POST"],
        "auth": "admin",
    },
    "doctor_detail": {
        "description": "View detailed information for a specific doctor.",
        "methods": ["GET"],
        "auth": "admin",
    },
    "doctor_edit": {
        "description": "Edit an existing doctor's profile and credentials.",
        "methods": ["GET", "POST"],
        "auth": "admin",
    },
    "doctor_delete": {
        "description": "Remove a doctor from the platform.",
        "methods": ["POST", "DELETE"],
        "auth": "admin",
    },
    "doctors_schedules": {
        "description": "Overview of all doctor schedules across the platform.",
        "methods": ["GET"],
        "auth": "admin",
    },
    "doctor_schedules": {
        "description": "View schedule for a specific doctor.",
        "methods": ["GET"],
        "auth": "admin",
    },
    "patient_list": {
        "description": "List all registered patients.",
        "methods": ["GET"],
        "auth": "admin",
    },
    "patient_add": {
        "description": "Register a new patient from the admin panel.",
        "methods": ["GET", "POST"],
        "auth": "admin",
    },
    "patient_medical_records": {
        "description": "View medical records for a specific patient.",
        "methods": ["GET"],
        "auth": "admin",
    },
    "appointment_list": {
        "description": "View today's and upcoming appointments.",
        "methods": ["GET"],
        "auth": "admin",
    },
    "appointment_history": {
        "description": "Browse historical appointment records.",
        "methods": ["GET"],
        "auth": "admin",
    },
    "appointment_add": {
        "description": "Create a new appointment from the admin panel.",
        "methods": ["GET", "POST"],
        "auth": "admin",
    },
    "medicine_list": {
        "description": "Admin list of all medicines in the catalog.",
        "methods": ["GET"],
        "auth": "admin",
    },
    "medicine_add": {
        "description": "Add a new medicine to the catalog.",
        "methods": ["GET", "POST"],
        "auth": "admin",
    },
    "medicine_edit": {
        "description": "Edit medicine details, pricing, and inventory info.",
        "methods": ["GET", "POST"],
        "auth": "admin",
    },
    "category_list": {
        "description": "Manage medicine categories.",
        "methods": ["GET"],
        "auth": "admin",
    },
    "inventory_list": {
        "description": "View and manage medicine inventory levels.",
        "methods": ["GET"],
        "auth": "admin",
    },
    "sales_reports": {
        "description": "Sales analytics and revenue reports.",
        "methods": ["GET"],
        "auth": "admin",
    },
    "inventory_reports": {
        "description": "Inventory movement and stock level reports.",
        "methods": ["GET"],
        "auth": "admin",
    },
    "appoinment_reports": {
        "description": "Appointment statistics and booking trend reports.",
        "methods": ["GET"],
        "auth": "admin",
    },
    "appointments": {
        "description": "Patient view of their booked appointments.",
        "methods": ["GET"],
        "auth": "authenticated",
    },
    "appointment_book": {
        "description": "Book a new doctor appointment.",
        "methods": ["GET", "POST"],
        "auth": "authenticated",
    },
    "check_prescription": {
        "description": "Check prescription validity before booking.",
        "methods": ["GET", "POST"],
        "auth": "authenticated",
    },
    "doctor_login": {
        "description": "Doctor portal login page.",
        "methods": ["GET", "POST"],
        "auth": "public",
    },
    "doctor_logout": {
        "description": "Log out from the doctor portal.",
        "methods": ["GET"],
        "auth": "doctor",
    },
    "doctor_profile": {
        "description": "Doctor portal profile and settings.",
        "methods": ["GET"],
        "auth": "doctor",
    },
    "doctor_appointment_management": {
        "description": "Doctors manage their patient appointments.",
        "methods": ["GET"],
        "auth": "doctor",
    },
    "doctor_availability_management": {
        "description": "Doctors set and update their availability slots.",
        "methods": ["GET", "POST"],
        "auth": "doctor",
    },
    "doctor_earning": {
        "description": "Doctor earnings and payment history.",
        "methods": ["GET"],
        "auth": "doctor",
    },
    "doctor_prescription": {
        "description": "Create and manage patient prescriptions.",
        "methods": ["GET", "POST"],
        "auth": "doctor",
    },
    "doctor_profilr": {
        "description": "Public-facing doctor profile page for patients.",
        "methods": ["GET"],
        "auth": "public",
    },
    "cart": {
        "description": "View shopping cart with selected medicines.",
        "methods": ["GET"],
        "auth": "authenticated",
    },
    "cart_add": {
        "description": "Add a medicine item to the shopping cart.",
        "methods": ["POST"],
        "auth": "authenticated",
    },
    "medicines_list": {
        "description": "Browse the full medicine catalog with filters.",
        "methods": ["GET"],
        "auth": "public",
    },
    "medicine_details": {
        "description": "Detailed medicine information page.",
        "methods": ["GET"],
        "auth": "public",
    },
    "orders": {
        "description": "List all orders placed by the patient.",
        "methods": ["GET"],
        "auth": "authenticated",
    },
    "order_details": {
        "description": "Detailed view of a specific order.",
        "methods": ["GET"],
        "auth": "authenticated",
    },
    "order_checkout": {
        "description": "Checkout API to create an order and initiate payment.",
        "methods": ["POST"],
        "auth": "authenticated",
    },
    "verify_razorpay": {
        "description": "Verify Razorpay payment signature after checkout.",
        "methods": ["POST"],
        "auth": "authenticated",
    },
    "labtests_catalog": {
        "description": "Browse available lab tests and packages.",
        "methods": ["GET"],
        "auth": "public",
    },
    "labtests_booking_modal": {
        "description": "Lab test booking form and modal.",
        "methods": ["GET", "POST"],
        "auth": "authenticated",
    },
    "labtests_history": {
        "description": "Patient lab test booking history.",
        "methods": ["GET"],
        "auth": "authenticated",
    },
    "patient-resolve": {
        "description": "Resolve or create a patient account during authentication.",
        "methods": ["POST"],
        "auth": "public",
    },
    "auth-google": {
        "description": "Google OAuth login endpoint for patients.",
        "methods": ["POST"],
        "auth": "public",
    },
    "auth-logout": {
        "description": "API logout — clears JWT cookies.",
        "methods": ["POST"],
        "auth": "public",
    },
    "me": {
        "description": "Returns the currently authenticated user's profile.",
        "methods": ["GET"],
        "auth": "authenticated",
    },
    "admin-users-list": {
        "description": "List all admin users (ViewSet list action).",
        "methods": ["GET"],
        "auth": "admin",
    },
    "admin-users-detail": {
        "description": "Retrieve, update, or delete a specific admin user.",
        "methods": ["GET", "PUT", "PATCH", "DELETE"],
        "auth": "admin",
    },
    "admin-availability-create": {
        "description": "Create a doctor availability slot via API.",
        "methods": ["POST"],
        "auth": "admin",
    },
    "admin-appointment-book": {
        "description": "Book an appointment via API with payment checkout.",
        "methods": ["POST"],
        "auth": "authenticated",
    },
    "api_appointments": {
        "description": "Fetch doctor-grouped appointments with filters.",
        "methods": ["POST"],
        "auth": "authenticated",
    },
    "doctor_list_api": {
        "description": "Public API listing available doctors.",
        "methods": ["GET"],
        "auth": "public",
    },
    "medicine-list": {
        "description": "Paginated medicine catalog API with search and filters.",
        "methods": ["GET"],
        "auth": "public",
    },
    "token_refresh": {
        "description": "Refresh JWT access token using a valid refresh token.",
        "methods": ["POST"],
        "auth": "authenticated",
    },
    "schema": {
        "description": "OpenAPI schema definition for all API endpoints.",
        "methods": ["GET"],
        "auth": "public",
    },
    "swagger": {
        "description": "Interactive Swagger UI for exploring and testing APIs.",
        "methods": ["GET"],
        "auth": "public",
    },
}

CATEGORY_CONFIG = [
    {
        "id": "auth",
        "label": "Authentication",
        "icon": "fa-lock",
        "color": "#f59e0b",
        "match": lambda path, name: name in ("login", "logout", "send_otp", "verify_otp", "doctor_login", "doctor_logout", "admin_login", "admin_logout", "patient-resolve", "auth-google", "auth-logout", "token_refresh", "me"),
    },
    {
        "id": "admin",
        "label": "Admin Panel",
        "icon": "fa-shield-halved",
        "color": "#ef4444",
        "match": lambda path, name: path.startswith("admin/"),
    },
    {
        "id": "doctor-portal",
        "label": "Doctor Portal",
        "icon": "fa-user-md",
        "color": "#0ea5e9",
        "match": lambda path, name: path.startswith("doctor/"),
    },
    {
        "id": "api",
        "label": "REST API",
        "icon": "fa-code",
        "color": "#6366f1",
        "match": lambda path, name: path.startswith("api/"),
    },
    {
        "id": "appointments",
        "label": "Appointments",
        "icon": "fa-calendar-check",
        "color": "#10b981",
        "match": lambda path, name: "appointment" in path or "availability" in path or "prescription" in path,
    },
    {
        "id": "medistore",
        "label": "Pharmacy & Cart",
        "icon": "fa-pills",
        "color": "#8b5cf6",
        "match": lambda path, name: "medicine" in path or "cart" in path or "inventory" in path or "categor" in path,
    },
    {
        "id": "orders",
        "label": "Orders & Payments",
        "icon": "fa-credit-card",
        "color": "#ec4899",
        "match": lambda path, name: "order" in path or "payment" in path or "checkout" in path or "razorpay" in path,
    },
    {
        "id": "labtests",
        "label": "Lab Tests",
        "icon": "fa-flask",
        "color": "#06b6d4",
        "match": lambda path, name: "lab" in path or "test" in path,
    },
    {
        "id": "public",
        "label": "Public Pages",
        "icon": "fa-globe",
        "color": "#667eea",
        "match": lambda path, name: True,
    },
]

AUTH_LABELS = {
    "public": {"label": "Public", "class": "auth-public"},
    "authenticated": {"label": "Auth Required", "class": "auth-required"},
    "admin": {"label": "Admin", "class": "auth-admin"},
    "doctor": {"label": "Doctor", "class": "auth-doctor"},
}

METHOD_COLORS = {
    "GET": "#10b981",
    "POST": "#3b82f6",
    "PUT": "#f59e0b",
    "PATCH": "#8b5cf6",
    "DELETE": "#ef4444",
}
