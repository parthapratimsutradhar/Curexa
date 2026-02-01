from apps.medistore.models.medicines_model import Medicine

def get_all_medicines():
    return Medicine.objects.all()

def add_new_medicine(
    *,
    SKU,
    name,
    category,
    cost_price,
    retail_price,
    images_path,
    is_prescription_required=False,
    classification=None,
    age_group=None,
    salt_composition=None,
    dosage_strength=None,
    manufacturer=None,
    manufacture_date=None,
    description=None,
    expiry_date=None,
):
    medicine = Medicine.objects.create(
        SKU=SKU,
        name=name,
        category=category,
        cost_price=cost_price,
        retail_price=retail_price,
        medicine_images=images_path,
        is_prescription_required=is_prescription_required,
        classification=int(classification) if classification else None,
        age_group=int(age_group) if age_group else None,
        salt_composition=salt_composition,
        dosage_strength=dosage_strength,
        manufacturer=manufacturer,
        manufacture_date=manufacture_date,
        description=description,
        expiry_date=expiry_date,
    )
    return medicine

