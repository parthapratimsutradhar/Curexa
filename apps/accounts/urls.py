from apps.accounts import views
from django.urls import path


urlpatterns = [
    # Home URL
    path('', views.HomeView.as_view(), name='home'),
    
    # Authentication URLs
    # path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('send-otp/', views.send_otp_view, name='send_otp'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    
    # Account
    path('profile/', views.ProfileView.as_view(), name='profile')

]
