from apps.core import views
from django.urls import path

urlpatterns = [
    path('docs/', views.RouteDocumentationView.as_view(), name='route_documentation'),
    path('emergency/', views.EmergencyView.as_view(), name='emergency_care'),
    path('about/', views.AboutView.as_view(), name='about'),
    path("chat/", views.chat_page, name="chat_page"),
    path("chat/api/", views.chat_api, name="chat_api"),

]

