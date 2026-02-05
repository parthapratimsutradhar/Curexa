from apps.orders import views
from django.urls import path

urlpatterns = [
    
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('order/<int:pk>/details', views.OrderDetailsView.as_view(), name='order_details'),
    
]

