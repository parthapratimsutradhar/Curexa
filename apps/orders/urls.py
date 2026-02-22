from apps.orders import views
from django.urls import path

urlpatterns = [
    # orders
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('orders/<int:pk>/details', views.OrderDetailsView.as_view(), name='order_details'),
    path('orders/checkout', views.CheckoutOrderAPIView.as_view(), name='order_checkout'),

    # Invoice
    
    # Payment    
    path("payment/verify-razorpay", views.verify_razorpay_payment, name="verify_razorpay"),


]
    
