from apps.medistore.models import Cart, CartItem
from decimal import Decimal, ROUND_HALF_UP
from apps.core.services.util_services import enum_name
from apps.core.constants.default_values import DosageForm

def get_or_create_cart(patient):
    cart, _ = Cart.objects.get_or_create(owner=patient)
    return cart

def get_cart_details(patient):
    cart = get_or_create_cart(patient)
    items = CartItem.objects.filter(cart=cart, is_active=True).select_related('medicine')
    
    GST_RATE = Decimal("12")  # 12% GST

    details = []
    subtotal = Decimal("0.00")

    for item in items:
        med = item.medicine
        if med.is_active:
            quantity = item.quantity
            retail_price = Decimal(med.retail_price)
            original_price = Decimal(med.original_price or med.retail_price)

            total_price = quantity * retail_price
            total_original_price = quantity * original_price

            discount = Decimal("0")
            if total_original_price > total_price:
                discount = ((total_original_price - total_price) * 100 / total_original_price).quantize(Decimal('1'), rounding=ROUND_HALF_UP)

            # Calculate total units
            try:
                units_per_pack = int(str(med.pack_size).strip())
            except:
                units_per_pack = 1  # fallback if not a number
            total_units = quantity * units_per_pack

            details.append({
                "cart_item_id": item.id,
                "quantity": quantity,
                "medicine_id": med.id,
                "name": med.name,
                "retail_price": retail_price * quantity,
                "original_price": original_price,
                "discount": discount,
                "total_price": total_price,
                "total_original_price": total_original_price,
                "description": med.description,
                "images": med.medicine_images,
                "pack_size": med.pack_size,
                "total_units": total_units,
                "dosage_name": enum_name(DosageForm, med.dosage_form).capitalize(),
                "manufacturer": med.manufacturer,
                "expiry_date": med.expiry_date,
                "is_prescription_required": med.is_prescription_required,
            })

            subtotal += total_price  # accumulate subtotal

    # Now calculate GST on the subtotal
    gst_amount = (subtotal * GST_RATE / 100).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    cgst = (gst_amount / 2).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    sgst = (gst_amount / 2).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    total = (subtotal + gst_amount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    return {
        "cart_id": cart.id,
        "owner": cart.owner.patient.get_full_name(),
        "items": details,
        "total_items": sum(item["quantity"] for item in details),
        "subtotal": subtotal,        # before GST
        "gst_amount": gst_amount,    # total GST
        "cgst": cgst,                # CGST
        "sgst": sgst,                # SGST
        "total_price": total,        # subtotal + GST
    }
    
def add_item(patient, medicine, quantity):
    cart = get_or_create_cart(patient)
    item, created = CartItem.objects.get_or_create(cart=cart, medicine=medicine, is_active=True)
    if not created:
        item.quantity += quantity
    else:
        item.quantity = quantity
    item.save()
    return item

def remove_item(patient, medicine):
    cart = get_or_create_cart(patient)
    try:
        item = CartItem.objects.get(cart=cart, medicine=medicine, is_active=True)
        item.is_active = False
        item.save()
    except CartItem.DoesNotExist:
        pass

def clear_cart(patient):
    cart = get_or_create_cart(patient)
    
    # Get all active cart items
    items = CartItem.objects.filter(cart=cart, quantity__gt=0)
    
    # Mark them as inactive
    for item in items:
        item.is_active = False
    
    # Bulk update the is_active field
    CartItem.objects.bulk_update(items, ['is_active'])
    
    
def cart_total(patient):
    cart = get_or_create_cart(patient)
    return sum(item.medicine.price * item.quantity for item in cart.items.all())