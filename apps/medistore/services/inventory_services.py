from apps.medistore.models.inventory_model import Inventory

def add_medicine(medicine, quantity, stock_alert_level):
    return Inventory.objects.create(
        medicine=medicine,
        quantity=quantity,
        stock_alert_level=stock_alert_level
    )
    
def overall_stock_percentage():
    inventories = Inventory.objects.all()

    total_quantity = sum(inv.quantity for inv in inventories)
    total_max = sum(max(inv.stock_alert_level, 1) for inv in inventories)  # avoid division by 0

    if total_max == 0:
        return 100 if total_quantity > 0 else 0

    percentage = int((total_quantity / total_max) * 100)
    return min(100, percentage)    