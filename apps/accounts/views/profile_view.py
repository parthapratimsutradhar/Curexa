from django.views import View
from django.shortcuts import redirect, render
from apps.accounts.services import patient_services, user_services

class ProfileView(View):
    def get(self, request):
        print(request)
        user=user_services.get_user_details(request.user.id)
        print("hiiiodnbnldnid:"+user)
        return render(request, "enduser/accounts/profile.html")
    
class EditProfileView(View):
    def get(self, request):
        return render(request, "enduser/accounts/edit_profile.html")