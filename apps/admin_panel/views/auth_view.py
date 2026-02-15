from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from apps.core.utilities.decorators import anonymous_required, admin_required
from apps.core.services.admin import admin_service
from apps.core.constants.default_values import Role
from apps.core.constants.error_message import ErrorMessages


@anonymous_required(redirect_url="/admin/" )
class AdminLoginView(View):    
    def get(self, request):        
        return render(request, 'admin/auth/admin_login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')        
        # Authentication logic here
        user = authenticate(request, email=email, password=password)
        # Check if authentication succeeded
        if user and getattr(user, "role", None) == Role.ADMIN.value:
            login(request, user)
            return redirect('admin_dashboard')                    
        return render(request, 'admin/auth/admin_login.html', {'error_message': ErrorMessages.E00001.value})
    
@admin_required(login_url="/admin/login/")    
class AdminLogoutView(View):
    def get(self, request):
        logout(request)        
        return redirect('admin_login')