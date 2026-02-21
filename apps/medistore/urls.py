from apps.medistore import views
from django.urls import path

urlpatterns = [
    # Cart
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add', views.AddToCartView.as_view(), name='cart_add'),
    
    # Medicine
    path('medicines/', views.MedicineListView.as_view(), name='medicines_list'),
    path('medicine/details/', views.MedicineDetailsView.as_view(), name='medicine_details'),
    
]

