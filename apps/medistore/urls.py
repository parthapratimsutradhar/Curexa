from apps.medistore import views
from django.urls import path

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('medicines/', views.MedicineListView.as_view(), name='medicines_list'),
    path('medicine/details/', views.MedicineDetailsView.as_view(), name='medicine_details'),
    
]

