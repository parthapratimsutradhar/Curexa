from apps.orders.models.orders_model import Order 
from apps.orders.models.order_item_model import OrderItem
from decimal import Decimal

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
    
    
    
from decimal import Decimal, ROUND_HALF_UP
from django.db import transaction
from apps.orders.models import Order, OrderItem
from apps.orders.services import create_invoice
from apps.orders.services.payment_service import create_razorpay_order

def checkout_cart(patient, cart_items, billing_address=None, tax_rate=Decimal("12")):
    """
    Complete checkout service: creates Order, OrderItems, Invoice, and Payment.
    Wrapped in a single atomic transaction.
    """
    if not cart_items:
        raise ValueError("Cart is empty")

    with transaction.atomic():
        # 1️⃣ Create Order
        total_amount = sum(Decimal(item["retail_price"]) * item["quantity"] for item in cart_items)
        order = Order.objects.create(patient=patient)

        # 2️⃣ Create OrderItems
        order_items_bulk = [
            OrderItem(
                order=order,
                medicine_id=item["medicine_id"],
                quantity=item["quantity"],
                price=Decimal(item["retail_price"])
            )
            for item in cart_items
        ]
        OrderItem.objects.bulk_create(order_items_bulk)

        # 3️⃣ Create Invoice
        invoice = create_invoice(
            patient=patient,
            content_object=order,
            billing_address=billing_address,
            subtotal=total_amount,
            tax_rate=tax_rate
        )

        # 4️⃣ Create Payment (Razorpay/Stripe)
        payment_data = create_razorpay_order(invoice.id)  # Returns payment info (order_id/session_id)

        return {
            "order_id": order.id,
            "invoice_id": invoice.id,
            "payment": payment_data
        }    