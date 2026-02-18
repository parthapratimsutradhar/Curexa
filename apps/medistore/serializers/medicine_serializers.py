from rest_framework import serializers
from apps.medistore.models import Medicine
from apps.medistore.serializers import category_serializers, inventory_serializers
from apps.core.utilities.cloudinary_utils import cloudinary_upload_files

class MedicineListSerializer(serializers.ModelSerializer):
    category = category_serializers.CategorySerializer(read_only=True)
    inventory = inventory_serializers.InventorySerializer(read_only=True)

    dosage_form_display = serializers.CharField(
        source="get_dosage_form_display",
        read_only=True
    )

    age_group_display = serializers.CharField(
        source="get_age_group_display",
        read_only=True
    )
    
    stock_status = serializers.CharField(read_only=True)  # comes from annotation
     # 🔹 Include annotated field
    in_stock = serializers.BooleanField(read_only=True)


    class Meta:
        model = Medicine
        fields = [
            "id",
            "SKU",
            "name",
            "retail_price",
            "medicine_images",
            "is_prescription_required",
            "category",
            "dosage_form",
            "dosage_form_display",
            "age_group",
            "age_group_display",
            "salt_composition",
            "dosage_strength",
            "manufacturer",
            "manufacture_date",
            "expiry_date",
            "description",
            "inventory",
            "is_active",
            "created_at",
            "in_stock",  # 🔹 include here
            "stock_status"
        ]


class MedicineImageUploadSerializer(serializers.Serializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        allow_empty=False
    )

    def update(self, instance, validated_data):
        """
        Uploads images to Cloudinary and appends URLs to instance.medicine_images
        """
        files = validated_data.get("images", [])
        uploaded_urls = cloudinary_upload_files(files, folder_name=f"medicines/{instance.SKU}")

        # Append new URLs to existing images
        instance.medicine_images = (instance.medicine_images or []) + uploaded_urls
        instance.save()
        return instance
