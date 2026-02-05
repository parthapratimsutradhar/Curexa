from django.views import View
from django.shortcuts import redirect, render

class ProfileView(View):
    def get(self, request):
        return render(request, "enduser/accounts/profile.html")
    
class EditProfileView(View):
    def get(self, request):
        return render(request, "enduser/accounts/edit_profile.html")