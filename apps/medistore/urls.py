from apps.medistore import views
from django.urls import path

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    
]

