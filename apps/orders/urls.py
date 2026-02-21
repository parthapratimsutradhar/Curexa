from apps.orders import views
from django.urls import path

urlpatterns = [
    # orders
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('order/<int:pk>/details', views.OrderDetailsView.as_view(), name='order_details'),
    path('order/create', views.OrderCreateView.as_view(), name='order_create'),
    
    
    path('order/checkout', views.CheckoutOrderAPIView.as_view(), name='order_checkout'),
    
    path('test-razorpay/', views.test_razorpay_order, name='test_order'),
    path('testpage/', views.testpage.as_view(), name='test_page'),

    # Invoice
    path('invoice/create', views.InvoiceCreateView.as_view(), name='invoice_create'),
    
    # Payment
    path('payment/create', views.CreatePaymentAPIView.as_view(), name='payment_create'),


]
    
