from apps.orders import views
from django.urls import path

urlpatterns = [
    
    path('orders/', views.OrderListView.as_view(), name='orders'),
    
]

