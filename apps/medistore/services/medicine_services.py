from apps.medistore.models.medicines_model import Medicine
from django.db.models import Count
from apps.core.constants.default_values import AGE_GROUP, DosageForm
from apps.core.services.util_services import enum_name

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
        dosage_form=int(classification) if classification else None,
        age_group=int(age_group) if age_group else None,
        salt_composition=salt_composition,
        dosage_strength=dosage_strength,
        manufacturer=manufacturer,
        manufacture_date=manufacture_date,
        description=description,
        expiry_date=expiry_date,
    )
    return medicine

def medicine_count():
    Medicine.objects.all().count()

def medicine_count_by_category():
    return (
        Medicine.objects
        .values('category__id', 'category__name')
        .annotate(total=Count('id'))
        .order_by('category__name')
    )


def medicine_count_by_dosage():
    qs = Medicine.objects.values('dosage_form') \
                         .annotate(total=Count('id'))

    # Map enum value to both name and value
    return [
        {
            'dosage_form_name': enum_name(DosageForm, item['dosage_form']),
            'dosage_form_value': item['dosage_form'],
            'total': item['total']
        }
        for item in qs
    ]


def medicine_count_by_age():
    qs = Medicine.objects.values('age_group') \
                         .annotate(total=Count('id'))

    # Map enum value to both name and value
    return [
        {
            'id':item['age_group'],
            'age_group_name': enum_name(AGE_GROUP, item['age_group']),
            'age_group_value': item['age_group'],
            'total': item['total']
        }
        for item in qs
    ]

