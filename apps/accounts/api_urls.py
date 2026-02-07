from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.accounts import views
from apps.accounts.views.admin_user_viewset import AdminUserViewSet

router = DefaultRouter()
router.register(r'admin-users', AdminUserViewSet, basename='admin-users')

urlpatterns = [
    path("auth/patient/resolve/", views.PatientResolveAPIView.as_view(), name="patient-resolve"),
    path('', include(router.urls)),
]
