from apps.accounts import views
from django.urls import path


urlpatterns = [
    # Home URL
    path('', views.HomeView.as_view(), name='home'),
    
    # Authentication URLs
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('send-otp/', views.send_otp_view, name='send_otp'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    
    # Account
    path('profile/', views.ProfileView.as_view(), name='patient-profile'),
    path('profile/edit/', views.EditProfileView.as_view(), name='profile_edit'),
    
    
    path('medicine/', views.EditProfileView.as_view(), name='medicine-catalog'),
    path('services/', views.EditProfileView.as_view(), name='care-services'),
    path('health/', views.EditProfileView.as_view(), name='health-dashboard'),
    path('emergency/', views.EditProfileView.as_view(), name='emergency-care'),
    path('about/', views.EditProfileView.as_view(), name='about'),
    path('cart/', views.EditProfileView.as_view(), name='cart'),
    path('orders/', views.EditProfileView.as_view(), name='my-orders'),
    path('appointments/', views.EditProfileView.as_view(), name='appointments'),

]
