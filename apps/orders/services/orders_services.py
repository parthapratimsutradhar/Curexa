from apps.orders.models.orders_model import Order 
from apps.orders.models.order_item_model import OrderItem
from decimal import Decimal
from apps.medistore.services import cart_services

def order_create(patient, ):
    return Order.objects.create(
            patient=patient
        )


def bulk_create_order_items(order, items):
    """
    Bulk create OrderItem instances for a given order.

    Args:
        order: Order instance to attach the items to
        items: list of dicts with keys 'medicine_id', 'quantity', 'retail_price'
    
    Example:
        items = [
            {"medicine_id": 1, "quantity": 2, "retail_price": "245.00"},
            {"medicine_id": 2, "quantity": 1, "retail_price": "32.50"},
        ]
    """
    order_items_bulk = []
    for item in items:
        order_items_bulk.append(OrderItem(
            order=order,
            medicine_id=item["medicine_id"],
            quantity=item["quantity"],
            price=Decimal(item["retail_price"])
        ))
    
    # Bulk create all items in one query
    OrderItem.objects.bulk_create(order_items_bulk)
    
    
    
from django.db import transaction
from apps.orders.services import create_invoice
from apps.orders.services.payment_service import create_razorpay_order


def checkout_cart(patient, cart_items):
    if not cart_items.exists():
        raise ValueError("Cart is empty")

    with transaction.atomic():

        # 1️⃣ Create Order
        order = Order.objects.create(patient=patient)

        subtotal = Decimal("0.00")

        # 2️⃣ Create OrderItems & calculate subtotal
        for cart_item in cart_items.select_related("medicine"):
            unit_price = cart_item.medicine.retail_price

            order_item = OrderItem.objects.create(
                order=order,
                medicine=cart_item.medicine,
                quantity=cart_item.quantity,
                unit_price=unit_price
            )

            subtotal += order_item.total_price

        # 3️⃣ Tax calculation
        TAX_RATE = Decimal("12.00")
        tax_amount = (subtotal * TAX_RATE) / Decimal("100")
        total_amount = subtotal + tax_amount
        
        cart_services.clear_cart(patient)

        # 4️⃣ Create Invoice (explicit FK)
        invoice = create_invoice(
            patient=patient,
            order=order,
            subtotal=subtotal,
            tax_rate=TAX_RATE
        )

        # 5️⃣ Clear cart
        cart_items.delete()

        # 6️⃣ Create Razorpay Order + Payment
        payment_payload = create_razorpay_order(invoice)

        return payment_payload