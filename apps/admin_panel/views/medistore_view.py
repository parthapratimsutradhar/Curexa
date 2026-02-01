from django.views import View
from django.shortcuts import render, redirect
from apps.medistore.services import category_services
from apps.core.services import util_services
from apps.medistore.services import medicine_services, inventory_services,inventory_log_services
from apps.core.constants.default_values import DosageForm, AGE_GROUP
from apps.core.utilities import file_management

class MedicineListView(View):
    def get(self, request):
        return render(request, 'admin/medicens/medication_list.html')

class MedicineEditView(View):
    def get(self, request, pk):
        # Logic for editing a medication
        return render(request, 'admin/medicens/medication_details_edit.html')
    
    def post(self, request, pk):
        # Logic for saving the edited medication
        # This would typically involve form processing and saving to the database
        return redirect('medication_list')    

class MedicineAddView(View):
    def get(self, request):
        categories = category_services.get_all_category()
        context = {
            "categories": categories,
            "dosage_form": util_services.enum_choices(DosageForm),
            "age_group": util_services.enum_choices(AGE_GROUP)
        }
        return render(request, 'admin/medicens/add_new_medication.html', context)

    def post(self, request):
        name = request.POST.get('name')
        SKU = request.POST.get('SKU')
        category_id = request.POST.get('category')

        manufacturer = request.POST.get('manufacturer')
        cost_price = request.POST.get('cost_price') or 0
        retail_price = request.POST.get('retail_price') or 0
        quantity = request.POST.get('change_quantity') or 0
        stock_alert = request.POST.get('stock_alert') or 0

        description = request.POST.get('description')
        is_prescription_required = request.POST.get('is_prescription_required') == 'true'

        classification = request.POST.get('classification')
        age_group = request.POST.get('age_group')
        salt_composition = request.POST.get('salt_composition')
        dosage_strength = request.POST.get('dosage_strength')

        manufacture_date = request.POST.get('manufacture_date') or None
        expiry_date = request.POST.get('expiry_date') or None

        images_data = request.FILES.getlist('images')
        print(images_data)
        images_path = file_management.save_uploaded_file(images_data, "Medicines")
        print(images_path)
        

        category = category_services.get_category(category_id)

        medicine = medicine_services.add_new_medicine(
            SKU=SKU,
            name=name,
            category=category,
            cost_price=cost_price,
            retail_price=retail_price,
            images_path=images_path,
            is_prescription_required=is_prescription_required,
            classification=classification,
            age_group=age_group,
            salt_composition=salt_composition,
            dosage_strength=dosage_strength,
            manufacturer=manufacturer,
            manufacture_date=manufacture_date,
            description=description,
            expiry_date=expiry_date,
        )

        inventory_services.add_medicine(medicine, quantity, stock_alert)
        inventory_log_services.add_log(medicine, quantity, request.user)

        return redirect('medicine_list')

