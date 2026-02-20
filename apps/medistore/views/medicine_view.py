from django.views import View
from django.shortcuts import render, redirect
from apps.medistore.services import medicine_services, category_services, inventory_services
from apps.medistore.models import Medicine
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from apps.medistore.models import Medicine
from apps.medistore.serializers.medicine_serializers import MedicineListSerializer
from rest_framework.permissions import AllowAny
from django.db.models import F, Case, When, Value, CharField
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from decimal import Decimal
import json

class MedicineListView(View):
    def get(self, request):
        context = {
            'total_medicine':medicine_services.medicine_count(),
            "stock_percentage":inventory_services.overall_stock_percentage(),
            "support_24x7": '24/7',
            'category':medicine_services.medicine_count_by_category(),
            'dosage_form':medicine_services.medicine_count_by_dosage(),
            'age_group':medicine_services.medicine_count_by_age(),
            'slug':category_services.get_all_slug()
        }
        
        print(context["total_medicine"])

        return render (request, "enduser/medistore/medicine_products_catalog.html", context)
    
class MedicineDetailsView(View):
    def get(self, request):
        medicine_id = self.request.GET.get('id')
        medicine_data=medicine_services.get_medicine_details_id(medicine_id)
        print(medicine_data.uses_benefits)
        print(medicine_data.how_to_use)
        print(medicine_data.safety_info)
        return render(request, 'enduser/medistore/medicine_detail.html', {'medicine': medicine_data})       


class MedicinePagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = "page_size"
    max_page_size = 50
    page_query_param = "page"


class MedicineListAPIView(ListAPIView):
    serializer_class = MedicineListSerializer
    pagination_class = MedicinePagination   # ✅ added
    filter_backends = [SearchFilter, OrderingFilter]

    search_fields = [
        "name",
        "SKU",
        "salt_composition",
        "manufacturer",
        "category__name",
        "slug"
    ]
    ordering_fields = ["retail_price", "name", "created_at"]
    permission_classes = [AllowAny]
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = (
            Medicine.objects
            .select_related("category", "inventory")
            .filter(is_active=True)
            .annotate(
                stock_status=Case(
                    When(
                        inventory__quantity__gt=F("inventory__stock_alert_level"),
                        then=Value("IN_STOCK")
                    ),
                    When(
                        inventory__quantity__gt=0,
                        inventory__quantity__lte=F("inventory__stock_alert_level"),
                        then=Value("LOW_STOCK")
                    ),
                    default=Value("OUT_OF_STOCK"),
                    output_field=CharField()
                )
            )
        )
        
        params = self.request.query_params

        if params.get("category"):
            print("category")
            queryset = queryset.filter(category_id=params["category"])
            
        if params.get("generic"):
            print("generic")
            queryset = queryset.filter(is_generic=params["generic"])    

        if params.get("slug"):
            print("slug")
            queryset = queryset.filter(category__slug=params["slug"])

        if params.get("min_price"):
            print("min_price")
            queryset = queryset.filter(retail_price__gte=Decimal(params["min_price"]))

        if params.get("max_price"):
            print("max_price")
            queryset = queryset.filter(retail_price__lte=Decimal(params["max_price"]))


        if params.get("dosage_form"):
            print("dosage_form")
            queryset = queryset.filter(dosage_form=params["dosage_form"])

        if params.get("age_group"):
            print("age_group")
            queryset = queryset.filter(age_group=params["age_group"])

        if params.get("prescription_required") in ["true", "false"]:
            print("prescription_required")
            queryset = queryset.filter(
                is_prescription_required=params["prescription_required"] == "true"
            )
            
        if params.get("stock_status"):
            print("stock_status")
            status = params["stock_status"]

            if status == "IN_STOCK":
                queryset = queryset.filter(
                    inventory__quantity__gt=F("inventory__stock_alert_level")
                )
            elif status == "LOW_STOCK":
                queryset = queryset.filter(
                    inventory__quantity__gt=0,
                    inventory__quantity__lte=F("inventory__stock_alert_level")
                )
            elif status == "OUT_OF_STOCK":
                queryset = queryset.filter(inventory__quantity__lte=0)

        for obj in queryset:
            print(obj)


        return queryset
