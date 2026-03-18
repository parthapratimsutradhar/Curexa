from django.urls import path, include
from apps.labtests import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),

]
