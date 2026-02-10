from django.views import View
from django.shortcuts import render, redirect
from apps.medistore.services import medicine_services
from apps.medistore.models import Medicine
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from apps.medistore.models import Medicine

from apps.medistore.serializers.medicine_serializers import MedicineListSerializer

class MedicineListView(View):
    def get(self, request):
        return render (request, "enduser/medistore/medicine_products_catalog.html")
    
class MedicineDetailsView(View):
    def get(self, request):
        return render(request, "enduser/medistore/medicine_detail.html")        


class MedicineListAPIView(ListAPIView):
    serializer_class = MedicineListSerializer

    # Enable search only for this view
    filter_backends = [SearchFilter]

    search_fields = [
        "name",
        "SKU",
        "salt_composition",
        "manufacturer",
        "category__name",
    ]

    ordering_fields = [
        "retail_price",
        "name",
        "created_at",
        "expiry_date",
    ]

    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = (
            Medicine.objects
            .select_related("category")
            .prefetch_related("inventory")
            .filter(is_active=True)
        )

        # 🔹 Manual filters (query params)
        params = self.request.query_params

        if params.get("category"):
            queryset = queryset.filter(category_id=params["category"])

        if params.get("min_price"):
            queryset = queryset.filter(retail_price__gte=params["min_price"])

        if params.get("max_price"):
            queryset = queryset.filter(retail_price__lte=params["max_price"])

        if params.get("classification"):
            queryset = queryset.filter(classification=params["classification"])

        if params.get("age_group"):
            queryset = queryset.filter(age_group=params["age_group"])

        if params.get("prescription_required") is not None:
            queryset = queryset.filter(
                is_prescription_required=params["prescription_required"].lower() == "true"
            )

        return queryset
