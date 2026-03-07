"""
URL configuration for Curexa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from apps.core.views.core_view import not_found_page

urlpatterns = [
    # CBV and FBV URLs
    path('', include('apps.accounts.urls')),
    path('', include('apps.core.urls')),
    path('', include('apps.admin_panel.urls')),
    path('', include('apps.docbook.urls')),
    path('', include('apps.doctors.urls')),
    path('', include('apps.medistore.urls')),
    path('', include('apps.orders.urls')),
    path('', include('apps.labtests.urls')),
    
    # API URLs
    path('api/', include('apps.accounts.api_urls')),
    path('api/', include('apps.core.api_urls')),
    path('api/', include('apps.admin_panel.api_urls')),
    path('api/', include('apps.docbook.api_urls')),
    path('api/', include('apps.doctors.api_urls')),
    path('api/', include('apps.medistore.api_urls')),
    path('api/', include('apps.orders.api_urls')),

    # JWT Token Refresh
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    re_path(r"^(?P<path>.*)$", not_found_page, name="not_found_page"),
]
