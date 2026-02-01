from apps.medistore.models.inventory_model import Inventory

def add_medicine(medicine, quantity, stock_alert_level):
    return Inventory.objects.create(
        medicine=medicine,
        quantity=quantity,
        stock_alert_level=stock_alert_level
    )