from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse
from apps.core.utilities.otp_service import send_otp_code, verify_otp_code
from django.contrib.auth import login, logout
from apps.accounts.services import user_services

class LoginView(View):
    def get(self, request):
        return render(request, "auth/login.html")

    def post(self, request):
        # Handle login logic here
        return redirect('home')  # Redirect to home after login  
      

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')

def send_otp_view(request):
    if request.method == "POST":
        contact = request.POST.get("contact")
        if not contact:
            return JsonResponse({"status": "error", "message": "Contact required"}, status=400)
        
        send_otp_code(contact, purpose="login")  # can be signup, reset_password, etc.
        return JsonResponse({"status": "success", "message": "OTP sent successfully"})

def verify_otp_view(request):
    if request.method == "POST":
        contact = request.POST.get("contact")
        otp_code = request.POST.get("otp")

        if not contact or not otp_code:
            return JsonResponse({"status": "error", "message": "Missing fields"}, status=400)

        if verify_otp_code(contact, otp_code, purpose="login"):
            
             # Create or fetch user
            user = user_services.user_create_or_check(contact)
            
            patient_profile = user_services.ensure_user_profile(user)        

            # Log the user in (sets session cookie)
            login(request, patient_profile.user)
            
            # OTP verified successfully
            return JsonResponse({"status": "success", "message": "OTP verified"})            
        else:
            return JsonResponse({"status": "error", "message": "Invalid or expired OTP"}, status=400)


class VerifyOtpView(View):
    def get(self, request):
        return render(request, "auth/verify_otp.html")


class RegisterView(View):
    def get(self, request):
        return render(request, "auth/register.html")